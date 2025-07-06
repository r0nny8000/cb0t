import time
import pandas as pd


from kraken.spot import Market
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import


class AssetException(Exception):
    """Custom exception for market data errors."""


class Asset():

    pair = None
    df_1d = None
    df_1w = None

    intervals_to_min = {'1m': 1, '5m': 5, '15m': 15, '30m': 30,
                        '1h': 60, '4h': 240, '1d': 1440, '1w': 10080, '2w': 21600}

    def __init__(self, pair: str):
        self.pair = pair
        self.df_1d = self.get_ohlc(pair, '1d', 720)
        self.df_1w = self.get_ohlc(pair, '1w', 720)

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

    def get_asset_price(self) -> float:
        """ Fetches the current value for a given currency pair. """
        try:
            ticker = Market().get_ticker(self.pair)

            for v in ticker.values():
                return float(v['c'][0])

        except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
            raise AssetException(str(e).replace('\n', ' ')) from e

    def calculate_rsi(self, window: int = 14) -> pd.DataFrame:
        self.df_1d['change'] = self.df_1d['close'].astype(float).diff()
        self.df_1d['gain'] = self.df_1d.change.mask(self.df_1d.change < 0, 0.0)
        self.df_1d['loss'] = - \
            self.df_1d.change.mask(self.df_1d.change > 0, -0.0)

        # Calculate average gain and loss
        self.df_1d['avg_gain'] = self.df_1d['gain'].rolling(
            window=window, min_periods=window).mean()
        self.df_1d['avg_loss'] = self.df_1d['loss'].rolling(
            window=window, min_periods=window).mean()

        self.df_1d['rs'] = self.df_1d.avg_gain / \
            self.df_1d.avg_loss
        self.df_1d['rsi'] = 100 - (100 / (1 + self.df_1d.rs))

        return self.df_1d

    def calculate_sma(self, window: int = 50) -> pd.DataFrame:
        """Calculates and returns the Simple Moving Average (SMA) of the data."""
        column_name = 'sma_' + str(window)

        self.df_1d[column_name] = self.df_1d['close'].astype(float).rolling(
            window=window, min_periods=window).mean()
        self.df_1w[column_name] = self.df_1w['close'].astype(float).rolling(
            window=window, min_periods=window).mean()

        return self.df_1d

    def RSI_below(self, threshold: int = 50) -> bool:
        """Returns True if RSI is below the given value."""

        if 'rsi' not in self.df_1d.columns:
            self.calculate_rsi()

        return self.df_1d['rsi'].iloc[-1] < threshold

    def RSI_above(self, threshold: int = 50) -> bool:
        return not self.RSI_below(threshold)

    def price_below_weekly_SMA(self, window: int) -> bool:
        """Calculates and returns the SMA of the data."""
        column_name = 'sma_' + str(window)

        if column_name not in self.df_1w.columns:
            self.calculate_sma(window)

        return self.get_asset_price() < self.df_1w[column_name].iloc[-1]

    def price_above_weekly_SMA(self, window: int) -> bool:
        """Calculates and returns the SMA of the data."""
        return not self.price_below_weekly_SMA(window)
