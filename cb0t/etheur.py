"""
Module for the BTCUSD asset representation, extending the Asset class for the BTC/USD trading pair.
"""
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset


class ETHEUR(Asset):
    """Represents the ETHEUR asset."""

    def __init__(self):
        """Initializes the ETHEUR asset with the given pair."""
        super().__init__("XETHZEUR")
