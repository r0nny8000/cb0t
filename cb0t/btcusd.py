"""
Module for the BTCUSD asset representation, extending the Asset class for the BTC/USD trading pair.
"""
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset


class BTCUSD(Asset):
    """Represents the BTCUSD asset."""

    def __init__(self):
        """Initializes the BTCUSD asset with the given pair."""
        super().__init__("XXBTZUSD")
