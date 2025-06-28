import time

from kraken.spot import Market
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import


class AssetException(Exception):
    """Custom exception for market data errors."""


class Asset():

    pair = None
    data_daily = None
    data_weekly = None

    intervals_to_min = {'1m': 1, '5m': 5, '15m': 15, '30m': 30,
                        '1h': 60, '4h': 240, '1d': 1440, '1w': 10080, '2w': 21600}

    def __init__(self, pair: str):
        self.pair = pair
        self.data_daily = get_ohlc(self, pair, '1d', 720)
        self.data_weekly = get_ohlc(self, pair, '1w', 720)


def get_ohlc(self, pair: str, interval: str, length: int = 720):
    """Fetches OHLC (Open, High, Low, Close) data for a given currency pair
    and interval from the Kraken API.
    Returns at max 720 time steps per request.
    This is the defined maximum length for the Kraken API.
    """

    # Convert length to seconds
    since = time.time() - self.intervals_to_min[interval] * 60 * length

    try:
        ohlc = Market().get_ohlc(pair, self.intervals_to_min[interval], since)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError, KrakenInvalidArgumentsError) as e:
        raise AssetException(str(e).replace('\n', ' ')) from e

    data = []
    for v in ohlc.values():
        data = v
        break

    # Check if the data length matches the expected length if the interval is less than a week
    # for BTC there are no 720 candelsticks available on 2025-06-25
    # need to be changed in future if more data is available
    if len(data) != length and self.intervals_to_min[interval] < 10080:
        raise AssetException(
            f"Received {len(data)} data points for {pair} with interval {interval}, expected {length}.")

    return data
