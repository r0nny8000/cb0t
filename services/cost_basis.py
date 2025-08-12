"""Cost basis calculation service."""

import logging
from decimal import Decimal, getcontext
from assets.asset import Asset
from kraken.exceptions import KrakenUnknownAssetError
from utils.kraken_client import user

# Set decimal precision for financial calculations
getcontext().prec = 10


def calculate_cost_basis(asset: Asset, amount: float) -> float:
    """Calculates the cost basis for a given asset and amount."""

    # Fetch all trades for the user
    # 50 is the maximum number of trades to fetch in a single request
    # therefore we need to increase the offset and repeat the request until all trades are received
    try:
        all_trades = {}
        offset = 0

        while True:
            trades = user.get_trades_history(ofs=offset)

            if not trades or "trades" not in trades:
                break

            all_trades.update(trades["trades"])

            if len(trades["trades"]) < 50:
                break

            offset += 50

    except KrakenUnknownAssetError as e:
        logging.error(str(e))
        return None

    # now we have a complete list of trades for the asset
    # we start now calculating back the cost basis
    amount_counter = Decimal(str(amount))
    cost_basis = Decimal('0.0')

    # Iterate over all trades to calculate the cost basis
    logging.info(f"Calculating cost basis for {asset.pair} with amount {amount}")
    for trade_id, trade in all_trades.items():

        # Check if the trade is for the specified asset pair, skip otherwise
        if trade["pair"] == asset.pair:

            trade_vol = Decimal(str(trade["vol"]))
            trade_cost = Decimal(str(trade["cost"]))
            trade_fee = Decimal(str(trade["fee"]))

            logging.info(f"Processing start: {trade_id} {trade_vol} {trade_cost} {trade_fee} Counter: {amount_counter} Cost Basis: {cost_basis}")
            # If the trade is a buy, we subtract the volume from the amount counter
            if trade["type"] == "buy":

                # if the trade is bigger than the amount counter, we need to split the trade
                # to meet the remaining amount of the amount_counter
                if amount_counter < trade_vol:
                    cost_basis += ((trade_cost + trade_fee) * amount_counter) / trade_vol
                    amount_counter = 0

                else:
                    amount_counter -= trade_vol
                    cost_basis += (trade_cost + trade_fee)

                logging.info(f"Processing   buy: {trade_id} {trade_vol} {trade_cost} {trade_fee} Counter: {amount_counter} Cost Basis: {cost_basis}")

                if amount_counter == 0:
                    break


            elif trade["type"] == "sell":
                amount_counter += trade_vol
                cost_basis -= trade_cost
                logging.info(f"Processing  sell: {trade_id} {trade_vol} {trade_cost} {trade_fee} Counter: {amount_counter} Cost Basis: {cost_basis}")


    # Fees are already included in individual trades
    return round(float(cost_basis), 2)
