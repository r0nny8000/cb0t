"""
Module for the SOLUSD asset representation, extending the Asset class for the SOL/USD trading pair.
"""
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset


class PAXGEUR(Asset):
    """Represents the PAXGEUR  asset."""

    def __init__(self):
        """Initializes the PAXGEUR asset with the given pair."""
        super().__init__("PAXGEUR")
