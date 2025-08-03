"""
This module defines Azure Functions for an HTTP-triggered function and a timer-triggered function.
It demonstrates how to handle HTTP requests and execute periodic tasks using Azure Functions.
"""

# Provides logging capabilities to track events and debug the application.
import logging
import os
import json

import azure.functions as func  # Azure Functions Python library.
from jinja2 import Environment, FileSystemLoader
from kraken.spot import Market, User, Trade
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import

from cb0t.asset_pairs import *
from cb0t.asset import Asset

app = func.FunctionApp()


user = User(key=os.getenv('KRAKENAPIKEY'), secret=os.getenv('KRAKENAPISECRET'))
trade = Trade(key=os.getenv('KRAKENAPIKEY'), secret=os.getenv('KRAKENAPISECRET'))
env = os.getenv('CB0TENV', 'DEV')
env_schedule = {'DEV': '*/20 * * * * *', 'PROD': '0 0 16 * * *'}

# Set up the Jinja2 environment once, at the module level
template_dir = os.path.join(os.path.dirname(__file__), "cb0t/html/")
jinja_env = Environment(loader=FileSystemLoader(template_dir))


def print_json(obj: dict) -> None:
    """
    Prints a JSON object in a pretty format for debugging purposes.
    """
    print(json.dumps(obj, indent=4, default=str))


def html(template: str, *args, **kwargs) -> func.HttpResponse:
    """
    Renders the HTML template with the current environment and schedule.
    """
    template = jinja_env.get_template(template)
    return func.HttpResponse(template.render(*args, **kwargs), mimetype="text/html", status_code=200)


@app.route(route="{*path}", auth_level="anonymous", methods=["GET"])
def index(req: func.HttpRequest) -> func.HttpResponse:
    return html(template="index.html.j2", headers=req.method)


@app.route(route="ticker", auth_level="anonymous", methods=["GET"])
def get_ticker(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP triggered function to handle requests for the Kraken ticker.
    It retrieves the ticker information from the Kraken module and returns it as a JSON response.
    """

    # Extracting the 'pair' parameter from the request.
    pair = req.params.get('pair')

    if not pair:
        # Default to Bitcoin in EUR if no pair is provided.
        pair = 'XXBTZEUR,XETHZEUR,SOLEUR,PAXGEUR'

    # If 'pair' is provided, fetch the ticker information.
    logging.debug("Ticker function is processing with pair: %s", pair)

    try:

        ticker = Market().get_ticker(pair)
        assets = Market().get_asset_pairs(pair)
        asset_pair = Market().get_asset_pairs(pair)

        logging.debug('Ticker data: %s', ticker)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)

    return html(template="ticker.html.j2", pair=pair, ticker=ticker, assets=assets, asset_pair=asset_pair)

def calculate_cost_basis(asset: Asset, amount: float) -> float:
    """Calculates the cost basis for a given asset and amount."""

    try:

        # Fetch the asset's historical trades to calculate the cost basis.
        all_trades = {}
        offset = 0

        while True:

            trades = user.get_trades_history(ofs=offset)

            if not trades or 'trades' not in trades:
                break

            all_trades.update(trades['trades'])

            if len(trades['trades']) < 50:
                break

            offset += 50

    except KrakenUnknownAssetError as e:
        logging.error(str(e))
        return None

    # Filter trades for the specific asset pair.
    filtered_trades = {k: v for k, v in all_trades.items() if v['pair'] == asset.pair}


    amount_counter = amount
    cost_basis = 0.0

    # Iterate through the trades to calculate the cost basis.
    for trade_id, trade in all_trades.items():
        if trade['pair'] == asset.pair:
            if trade['type'] == 'buy':
                amount_counter -= float(trade['vol'])
                amount_counter = round(amount_counter, 8)
                cost_basis += float(trade['cost'])
                cost_basis += float(trade['fee'])
                #print (f"{asset.pair} {trade['vol']} at cost {trade['cost']} =>  Counter: {amount_counter} Cost basis: {cost_basis}")
                if amount_counter <= 0:
                    break
            elif trade['type'] == 'sell':
                amount_counter += float(trade['vol'])
                amount_counter = round(amount_counter, 8)
                cost_basis -= float(trade['cost'])
                cost_basis += float(trade['fee']) # every sell is increasing my cost basis too, as long as I hold the asset
                #print_json(trade)
                #print (f"{asset.pair} {trade['vol']} at win {trade['cost']} =>  Counter: {amount_counter} Cost basis: {cost_basis}")


    return cost_basis



@app.route(route="balance", auth_level="anonymous", methods=["GET"])
def get_balance(req: func.HttpRequest) -> func.HttpResponse:
    """Fetches and returns the account balance from Kraken."""
    account_balance = user.get_account_balance()


    asset_to_EUR_map = {
        'XXBT': BTCEUR(),
        'XETH': ETHEUR(),
        'SOL': SOLEUR(),
        'PAXG': PAXGEUR(),
    }

    balance = {}

    for asset, amount_str in account_balance.items():

        amount = float(amount_str)

        if amount == 0:
            continue

        if asset == 'ZEUR':
            balance[asset] = { 'amount': amount, 'price': amount, 'cost_basis': 0, 'average_price': 0, 'unrealized_pnl': 0, 'unrealized_pnl_pct': 0 }
            continue

        asset_pair = asset_to_EUR_map[asset]

        if asset_pair is None:
            logging.warning(f"No asset pair found for {asset}, skipping.")
            continue

        cost_basis = calculate_cost_basis(asset_pair, amount)

        balance[asset] = {
            'amount': amount,
            'price': amount * asset_pair.get_asset_price(),
            'cost_basis': cost_basis,
            'average_price': cost_basis / amount if amount > 0 else 0,
            'unrealized_pnl': asset_pair.get_asset_price() * amount - cost_basis,
            'unrealized_pnl_pct': ((asset_pair.get_asset_price() * amount - cost_basis) / cost_basis * 100) if cost_basis > 0 else 0
        }


    return html(template="balance.html.j2", balance=balance)


@app.route(route="env", auth_level="anonymous", methods=["GET"])
def get_env(req: func.HttpRequest) -> func.HttpResponse:
    """Fetches and returns the environment variables."""
    return html("env.html.j2", env=env)


@app.timer_trigger(schedule=env_schedule[env], arg_name="timer", run_on_startup=False, use_monitor=False)
def accumulate_assets(timer: func.TimerRequest) -> None:
    """Accumulates crypto periodically."""
    if timer.past_due:
        logging.info("The timer is past due! Will continue.")

    btceur = BTCEUR()
    accumulate(btceur, btceur.RSI_below(45) or btceur.below_Weekly_SMA(200), 8)

    etheur = ETHEUR()
    accumulate(etheur, etheur.RSI_below(40) or etheur.below_Weekly_SMA(250), 8)

    soleur = SOLEUR()
    accumulate(soleur, soleur.RSI_below(35), 8)

    paxgeur = PAXGEUR()
    accumulate(paxgeur, paxgeur.RSI_below(30), 8)



def accumulate(asset: Asset, condition: bool, euro: float) -> None:
    """
    Accumulates a specified cryptocurrency by checking the trend and bottom conditions.
    """
    if not condition:
        logging.info(f"{asset.pair} Skipping accumulation, conditions not met.")
        return

    try:

        logging.info(f"{asset.pair} Accumulating BTC.")

        # optimize the amount to accumulate based on the current price
        accelerated_euro = asset.accelerate(euro)
        volume = round(accelerated_euro / asset.get_asset_price(), 8)

        # check if minimum volume is met
        asset_pair = Market().get_asset_pairs(asset.pair)

        ordermin = float(asset_pair[asset.pair]['ordermin'])
        if volume < ordermin:
            logging.info('%s Volume %f is below minimum required %f, increasing volume.', asset.pair, volume, ordermin)
            volume = ordermin

        logging.info('%s Accumulating %f with %f EUR',
                     asset.pair, volume, accelerated_euro)

        # check if environment is set to PROD
        if env != 'PROD':
            raise RuntimeError(f'Not in production environment: {env}')

        # create order
        transaction = trade.create_order(ordertype='market',
                                         pair=asset.pair,
                                         side='buy',
                                         volume=volume)  # pylint: disable=line-too-long

        logging.info('%s Order created: %s', asset.pair, transaction)

    except Exception as e:  # pylint: disable=broad-except
        logging.error('%s %s', asset.pair, str(e).replace('\n', ' '))


