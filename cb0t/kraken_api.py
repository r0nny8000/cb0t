from kraken.spot import Market
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import


class KrakenAPIException(Exception):
    """Custom exception for Kraken API errors."""


def ticker(pair):
    """Fetches ticker data for a given trading pair from the Kraken API."""

    try:

        t = Market().get_ticker(pair)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        raise KrakenAPIException("Error fetching ticker data for %s: %s" % (
            pair, str(e).replace('\n', ' '))) from e

    return t
