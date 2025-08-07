"""Cost basis calculation service."""
import logging
from assets.asset import Asset
from kraken.exceptions import KrakenUnknownAssetError
from utils.kraken_client import user


def calculate_cost_basis(asset: Asset, amount: float) -> float:
    """Calculates the cost basis for a given asset and amount."""
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

    amount_counter = amount
    cost_basis = 0.0

    for trade_id, trade in all_trades.items():
        if trade["pair"] == asset.pair:
            if trade["type"] == "buy":
                amount_counter -= float(trade["vol"])
                amount_counter = round(amount_counter, 8)
                cost_basis += float(trade["cost"])
                cost_basis += float(trade["fee"])
                if amount_counter <= 0:
                    break
            elif trade["type"] == "sell":
                amount_counter += float(trade["vol"])
                amount_counter = round(amount_counter, 8)
                cost_basis -= float(trade["cost"])

    cost_basis = cost_basis * 1.004  # Adding kraken fee of 0.4%
    return round(cost_basis, 2)
