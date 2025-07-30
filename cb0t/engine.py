# -*- coding: utf-8 -*-
"""
This is the engine module for the cb0t trading bot, which interacts
with the Kraken API to fetch market data and perform calculations.
"""
import time

from kraken.spot import Market
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import


class EngineException(Exception):
    """Custom exception for market data errors."""


intervals_min = {'1m': 1, '5m': 5, '15m': 15, '30m': 30,
                 '1h': 60, '4h': 240, '1d': 1440, '1w': 10080, '2w': 21600}

intervals_sec = {'1m': 60, '5m': 300, '15m': 900, '30m': 1800,
                 '1h': 3600, '4h': 14400, '1d': 86400, '1w': 604800, '2w': 1209600}


def get_ohlc(pair: str, interval: str, length: int = 720):
    """Fetches OHLC (Open, High, Low, Close) data for a given currency pair
    and interval from the Kraken API.
    Returns at max 720 time steps per request.
    """

    # Convert length to seconds
    since = time.time() - intervals_sec[interval] * length

    try:
        ohlc = Market().get_ohlc(pair, intervals_min[interval], since)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError, KrakenInvalidArgumentsError) as e:
        raise EngineException(str(e).replace('\n', ' ')) from e

    data = []
    for v in ohlc.values():
        data = v
        break

    if len(data) != length:
        raise EngineException(
            f"Received {len(data)} data points, expected {length}.")

    return data


def get_sma(pair: str, interval: str, length: int) -> float:
    """
    Fetches the Simple Moving Average (SMA) for a given currency pair and interval.
    """
    ohlc = get_ohlc(pair, interval, length)

    if not ohlc:
        raise EngineException(f"No OHLC data received for {pair}.")

    sma = sum(float(candle[4]) for candle in ohlc) / length
    # Close price is at index 4

    if sma is None:
        raise EngineException(f"SMA calculation failed for {pair}.")

    return sma

