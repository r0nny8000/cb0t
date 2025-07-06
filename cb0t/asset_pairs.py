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


class BTCEUR(Asset):
    """Represents the BTCEUR asset."""

    def __init__(self):
        """Initializes the BTCEUR asset with the given pair."""
        super().__init__("XXBTZEUR")


class ETHUSD(Asset):
    """Represents the ETHUSD asset."""

    def __init__(self):
        """Initializes the ETHUSD asset with the given pair."""
        super().__init__("XETHZUSD")


class ETHEUR(Asset):
    """Represents the ETHEUR asset."""

    def __init__(self):
        """Initializes the ETHEUR asset with the given pair."""
        super().__init__("XETHZEUR")


class SOLUSD(Asset):
    """Represents the SOLUSD asset."""

    def __init__(self):
        """Initializes the SOLUSD asset with the given pair."""
        super().__init__("SOLUSD")


class SOLEUR(Asset):
    """Represents the SOLEUR asset."""

    def __init__(self):
        """Initializes the SOLEUR asset with the given pair."""
        super().__init__("SOLEUR")


class PAXGEUR(Asset):
    """Represents the PAXGEUR  asset."""

    def __init__(self):
        """Initializes the PAXGEUR asset with the given pair."""
        super().__init__("PAXGEUR")
