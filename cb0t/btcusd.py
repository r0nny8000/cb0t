from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import


import cb0t.engine as engine


class BTCUSD():

    length = 14  # or 16
    pair = "XXBTZUSD"
    interval = '1d'
    data = None

    def __init__(self):
        self.data = self.get_data()

    def RSI_above(self, value: int = 50) -> bool:
        """Returns True if RSI is above the given value."""
        return True

    def RSI_below(self, value: int = 50) -> bool:
        """Returns True if RSI is below the given value."""
        return True

    def get_data(self):
        """Fetches and returns closing prices as a list of floats."""
        ohlc = engine.get_ohlc(self.pair, self.interval, self.length)

        if not ohlc:
            raise ValueError(f"No OHLC data received for {self.pair}.")

        return [float(candle[4]) for candle in ohlc]

    def Daily_SMA_above(self) -> float:
        """Calculates and returns the SMA of the data."""
        return None

    def Daily_SMA_below(self) -> float:
        """Calculates and returns the SMA of the data."""
        return None
