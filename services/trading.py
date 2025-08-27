"""Trading and accumulation service."""
import os
import logging
from kraken.spot import Market
from assets.asset import Asset
from utils.kraken_client import trade


def accumulate(asset: Asset, euro: float) -> int:
    """Accumulates a specified cryptocurrency by adjusting volume based on distance to ATH."""

    try:
        logging.info(f"{asset.pair} Accumulating BTC.")

        accelerated_euro = asset.accelerate(euro)
        volume = round(accelerated_euro / asset.get_asset_price(), 8)

        asset_pair = Market().get_asset_pairs(asset.pair)
        ordermin = float(asset_pair[asset.pair]["ordermin"])

        if volume < ordermin:
            logging.info(
                f"{asset.pair} Volume {volume} is below minimum required {ordermin}, increasing volume."
            )
            volume = ordermin

        logging.info(f"{asset.pair} Accumulating {volume} with {accelerated_euro} EUR")

        env = os.getenv("CB0TENV", "DEV")
        if env != "PROD":
            raise RuntimeError(f"Not in production environment: {env}")

        transaction = trade.create_order(
            ordertype="market", pair=asset.pair, side="buy", volume=volume
        )

        logging.info(f"{asset.pair} Order created: {transaction}")
        return 1

    except Exception as e:
        logging.error(f"{asset.pair} {str(e).replace(chr(10), ' ')}")
        return 0
