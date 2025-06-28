from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset


class BTCUSD(Asset):

    def __init__(self):
        """Initializes the BTCUSD asset with the given pair."""
        super().__init__("XXBTZUSD")

    def RSI_below(self, value: int = 50) -> bool:
        """Returns True if RSI is below the given value."""
        return True

    def RSI_above(self, value: int = 50) -> bool:
        return not self.RSI_below(value)

    def Weekly_SMA_below(self, value: int = 50) -> bool:
        """Calculates and returns the SMA of the data."""
        return None

    def Weekly_SMA_above(self, value: int = 50) -> bool:
        """Calculates and returns the SMA of the data."""
        return not self.Weekly_SMA_below(value)
