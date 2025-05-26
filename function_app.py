"""
This module defines Azure Functions for an HTTP-triggered function and a timer-triggered function.
It demonstrates how to handle HTTP requests and execute periodic tasks using Azure Functions.
"""

# Provides logging capabilities to track events and debug the application.
import logging
import os
import cb0t.engine as engine
import azure.functions as func  # Azure Functions Python library.

# Jinja2 template engine for rendering HTML.
from jinja2 import Environment, FileSystemLoader

from kraken.spot import Market, User, Trade

from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import

import datetime

app = func.FunctionApp()


user = User(key=os.getenv('KRAKENAPIKEY'),
            secret=os.getenv('KRAKENAPISECRET'))
trade = Trade(key=os.getenv('KRAKENAPIKEY'),
              secret=os.getenv('KRAKENAPISECRET'))
env = os.getenv('CB0TENV', 'DEV')


# Set up the Jinja2 environment once, at the module level
template_dir = os.path.join(os.path.dirname(__file__), "cb0t/html/")
jinja_env = Environment(loader=FileSystemLoader(template_dir))


@app.route(route="ticker", auth_level="anonymous", )
def get_ticker(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP triggered function to handle requests for the Kraken ticker.
    It retrieves the ticker information from the Kraken module and returns it as a JSON response.
    """

    # Extracting the 'pair' parameter from the request.
    pair = req.params.get('pair')

    if not pair:
        return func.HttpResponse("Parameter 'pair' is required.", status_code=400)

    # If 'pair' is provided, fetch the ticker information.
    logging.info("Ticker function is processing with pair: %s", pair)

    try:

        ticker = Market().get_ticker(pair)
        assets = Market().get_asset_pairs(pair)
        logging.info('Ticker data: %s', ticker)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)

    # Render the HTML template with the ticker data.
    template = jinja_env.get_template("ticker.html")
    html = template.render(pair=pair, ticker=ticker, assets=assets)

    return func.HttpResponse(html, mimetype="text/html", status_code=200)


@app.route(route="balance", auth_level="anonymous")
def get_balance(req: func.HttpRequest) -> func.HttpResponse:
    """Fetches and returns the account balance from Kraken."""
    balance = user.get_account_balance()
    return func.HttpResponse(str(balance), mimetype="application/json", status_code=200)


@app.route(route="env", auth_level="anonymous")
def get_env(req: func.HttpRequest) -> func.HttpResponse:
    """Fetches and returns the environment variables."""
    return func.HttpResponse(str(env), mimetype="application/json", status_code=200)

# schedule: sec, min, hour, day, month, day_of_week


@app.timer_trigger(schedule="*/20 * * * * *", arg_name="timer", run_on_startup=False, use_monitor=False)
def accumulate_btc(timer: func.TimerRequest) -> None:
    """Accumulates crypto periodically."""
    if timer.past_due:
        logging.info("The timer is past due! Will continue.")
    accumulate('XXBTZEUR')  # Accumulate Bitcoin in EUR
    # accumulate('XETHZEUR')  # Accumulate Ethereum in EUR
    # accumulate('SOLEUR')  # Accumulate Solana in EUR


def accumulate(pair: str):

    # check conditions if trend is up or bottom is reached
    if not (engine.trend_is_up(pair) or engine.bottom_is_reached(pair)):
        logging.info('Trend and bottom conditions not met, skipping.')
        return

    investment = 8.0  # Amount to invest in EUR
    # optimize the amount to accumulate based on the current price

    # check if we have enough balance

    # increase limit if not in PROD

    # check if environment is set to PROD
    if env != 'PROD':
        logging.info('Running not in production environment: %s', env)
        return

    # create order
    # use order list to check if oder is filled for the day or a new order is needed
    # eg. run hourly, let the order open for 1h, if not filled, create a new with new parameters
    # if open higher that current price, set the limit lower, higher limit optherwise
    # or include volume into the decuision making
