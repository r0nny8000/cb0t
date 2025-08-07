"""Timer-triggered accumulation functions."""
import logging
import azure.functions as func
from cb0t.asset_pairs import BTCEUR, ETHEUR, SOLEUR, PAXGEUR
from services.trading import accumulate


def accumulate_assets(timer: func.TimerRequest) -> None:
    """Accumulates crypto periodically."""
    if timer.past_due:
        logging.info("The timer is past due! Will continue.")

    btceur = BTCEUR()
    accumulate(btceur, btceur.RSI_below(45) or btceur.below_Weekly_SMA(200), 8)

    etheur = ETHEUR()
    accumulate(etheur, etheur.RSI_below(40) or etheur.below_Weekly_SMA(250), 8)

    soleur = SOLEUR()
    accumulate(soleur, soleur.RSI_below(35), 4)

    paxgeur = PAXGEUR()
    accumulate(paxgeur, paxgeur.RSI_below(30), 8)
