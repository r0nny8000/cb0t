import time
import pandas as pd


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
        self.data_daily = self.get_ohlc(pair, '1d', 720)
        self.data_weekly = self.get_ohlc(pair, '1w', 720)

    def get_ohlc(self, pair: str, interval: str, length: int = 720):
        """Fetches OHLC (Open, High, Low, Close) data for a given currency pair
        and interval from the Kraken API.
        Returns at max 720 time steps per request.
        This is the defined maximum length for the Kraken API.
        """

        # Convert length to seconds
        since = time.time() - self.intervals_to_min[interval] * 60 * length

        try:
            ohlc = Market().get_ohlc(
                pair, self.intervals_to_min[interval], since)

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

        # Convert the data to a DataFrame
        df = pd.DataFrame(data, columns=[
            'time', 'open', 'high', 'low', 'close', 'vwap', 'volume', 'count'])

        # Convert the 'time' column to datetime format
        df['time'] = pd.to_datetime(df['time'], unit='s')

        return df

    def calculate_rsi(self, window: int = 14) -> pd.DataFrame:
        self.data_daily['change'] = self.data_daily['close'].astype(
            float).diff()
        self.data_daily['gain'] = self.data_daily.change.mask(
            self.data_daily.change < 0, 0.0)
        self.data_daily['loss'] = - \
            self.data_daily.change.mask(self.data_daily.change > 0, -0.0)

        # Calculate average gain and loss
        self.data_daily['avg_gain'] = self.data_daily['gain'].rolling(
            window=window, min_periods=window).mean()
        self.data_daily['avg_loss'] = self.data_daily['loss'].rolling(
            window=window, min_periods=window).mean()

        self.data_daily['rs'] = self.data_daily.avg_gain / \
            self.data_daily.avg_loss
        self.data_daily['rsi'] = 100 - (100 / (1 + self.data_daily.rs))

        return self.data_daily

    def RSI_below(self, threshold: int = 50) -> bool:
        """Returns True if RSI is below the given value."""

        if 'rsi' not in self.data_daily.columns:
            self.calculate_rsi()

        return self.data_daily['rsi'].iloc[-1] < threshold

    def RSI_above(self, threshold: int = 50) -> bool:
        return not self.RSI_below(threshold)

    def Weekly_SMA_below(self, threshold: int = 50) -> bool:
        """Calculates and returns the SMA of the data."""
        return None

    def Weekly_SMA_above(self, threshold: int = 50) -> bool:
        """Calculates and returns the SMA of the data."""
        return not self.Weekly_SMA_below(threshold)
