""" imports """
from cb0t.btcusd import BTCUSD


def test_init():
    """
    Unit tests for the BTCUSD class in the cb0t.btcusd module.
    """
    btcusd = BTCUSD()

    assert btcusd.pair == "XXBTZUSD"

    assert btcusd.data_daily is not None
    assert btcusd.data_weekly is not None
    assert isinstance(btcusd.data_daily, list)
    assert isinstance(btcusd.data_weekly, list)
    assert len(btcusd.data_daily) == 720  # defined my value of kraken
    assert len(btcusd.data_weekly) > 610


def test_RSI_above():
    """
    Test the RSI_above method of the BTCUSD class.
    """
    btcusd = BTCUSD()
    result = btcusd.RSI_above()

    assert isinstance(result, bool)
    assert result is True or result is False
