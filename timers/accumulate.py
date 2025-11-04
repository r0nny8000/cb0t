"""Timer-triggered accumulation functions."""

import logging
import azure.functions as func
from assets.asset_pairs import BTCEUR, ETHEUR, SOLEUR
from services.trading import accumulate


def accumulate_assets(timer: func.TimerRequest) -> None:
    """Accumulates crypto periodically and logs the number of assets accumulated."""
    if timer.past_due:
        logging.info("The timer is past due! Will continue.")

    assets_accumulated = 0

    btceur = BTCEUR()
    if btceur.RSI_below(40) or btceur.below_Weekly_SMA(200):
        assets_accumulated += accumulate(btceur, 8)

    etheur = ETHEUR()
    if etheur.RSI_below(35) or etheur.below_Weekly_SMA(200):
        assets_accumulated += accumulate(etheur, 8)

    # soleur = SOLEUR()
    # if (soleur.RSI_below(35)):
    #     assets_accumulated += accumulate(soleur, 4)

    logging.info(f"Total assets accumulated: {assets_accumulated}")

    # For timer functions, we can't return values directly
    # The result code will be 0 (success) if no exceptions are thrown
    # You can monitor the accumulation count in the logs
