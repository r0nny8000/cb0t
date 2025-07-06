"""
Module for the SOLUSD asset representation, extending the Asset class for the SOL/USD trading pair.
"""
from kraken.exceptions import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset


class SOLEUR(Asset):
    """Represents the SOLEUR asset."""

    def __init__(self):
        """Initializes the SOLEUR asset with the given pair."""
        super().__init__("SOLEUR")
