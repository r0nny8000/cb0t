from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset


class BTCUSD(Asset):

    def __init__(self):
        """Initializes the BTCUSD asset with the given pair."""
        super().__init__("XXBTZUSD")
