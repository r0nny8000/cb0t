"""Ticker-related HTTP routes."""
import logging
import azure.functions as func
from kraken.spot import Market
from kraken.exceptions import KrakenUnknownAssetError, KrakenUnknownAssetPairError
from utils.html_renderer import html


def get_ticker(req: func.HttpRequest) -> func.HttpResponse:
    """HTTP triggered function to handle requests for the Kraken ticker."""
    pair = req.params.get("pair")

    if not pair:
        pair = "XXBTZEUR,XETHZEUR,SOLEUR,PAXGEUR"

    logging.debug(f"Ticker function is processing with pair: {pair}")

    try:
        ticker = Market().get_ticker(pair)
        assets = Market().get_asset_pairs(pair)
        asset_pair = Market().get_asset_pairs(pair)

        logging.debug(f"Ticker data: {ticker}")

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)

    return html(
        template="ticker.html.j2",
        pair=pair,
        ticker=ticker,
        assets=assets,
        asset_pair=asset_pair,
    )
