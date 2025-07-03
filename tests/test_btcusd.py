""" imports """
from cb0t.btcusd import BTCUSD
from cb0t.asset import Asset


def test_init():
    """
    Unit tests for the BTCUSD class in the cb0t.btcusd module.
    """
    btcusd = BTCUSD()

    assert btcusd.pair == "XXBTZUSD"

    assert btcusd.data_daily is not None
    assert btcusd.data_weekly is not None
    assert len(btcusd.data_daily) == 720  # defined my value of kraken
    assert len(btcusd.data_weekly) > 610


def test_RSI_above():
    """
    Test the RSI_above method of the BTCUSD class.
    """
    btcusd = BTCUSD()
    assert 'time' in btcusd.data_daily
    assert 'close' in btcusd.data_daily
    assert 'rsi' not in btcusd.data_daily
    assert btcusd.RSI_below() in [True, False]
    assert 'rsi' in btcusd.data_daily
    assert btcusd.data_daily['rsi'].iloc[-1] < 100
    assert btcusd.data_daily['rsi'].iloc[-1] > 0
