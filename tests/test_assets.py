""" imports """
from cb0t.asset_pairs import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset


def print_dataframe(test_name, asset):
    """
    Prints the test name, and the last 4 rows of the asset's dataframes.
    """

    print(f"\n\nTesting {test_name} with pair: {asset.pair}")
    print("")
    print(asset.df_1d.tail(4))
    print("")
    print(asset.df_1w.tail(4))


def test_init():
    """
    Unit tests for the BTCUSD class in the cb0t.btcusd module.
    """
    btcusd = BTCUSD()

    assert btcusd.pair == "XXBTZUSD"

    assert btcusd.df_1d is not None
    assert btcusd.df_1w is not None
    assert len(btcusd.df_1d) == 720  # defined my value of kraken
    assert len(btcusd.df_1w) > 610

    print_dataframe("INIT", btcusd)


def test_rsi():
    """
    Test the RSI method of the BTCUSD class.
    """
    btcusd = BTCUSD()
    assert 'time' in btcusd.df_1d
    assert 'close' in btcusd.df_1d
    assert 'rsi' not in btcusd.df_1d
    assert btcusd.calculate_rsi() is not None
    assert 'rsi' in btcusd.df_1d
    assert btcusd.df_1d['rsi'].iloc[-1] < 100
    assert btcusd.df_1d['rsi'].iloc[-1] > 0

    print_dataframe("RSI", btcusd)

    assert btcusd.RSI_below(50) in [True, False]
    assert btcusd.RSI_above(50) in [True, False]

    rsi = btcusd.df_1d['rsi'].iloc[-1]
    assert rsi > 0 and rsi < 100
    assert btcusd.RSI_below(50) == (rsi < 50)
    assert btcusd.RSI_above(50) == (rsi > 50)


def test_sma():
    """
    Test the SMA method of the BTCUSD class.
    """

    # daily data frame
    btcusd = BTCUSD()
    assert 'time' in btcusd.df_1d
    assert 'close' in btcusd.df_1d
    assert 'time' in btcusd.df_1w
    assert 'close' in btcusd.df_1w

    assert 'sma_50' not in btcusd.df_1d
    assert 'sma_50' not in btcusd.df_1w
    assert btcusd.calculate_sma(50) is not None
    assert 'sma_50' in btcusd.df_1d
    assert 'sma_50' in btcusd.df_1w

    assert 'sma_200' not in btcusd.df_1d
    assert 'sma_200' not in btcusd.df_1w
    assert btcusd.calculate_sma(200) is not None
    assert 'sma_200' in btcusd.df_1d
    assert 'sma_200' in btcusd.df_1w

    print_dataframe("SMA", btcusd)

    assert btcusd.price_below_weekly_SMA(50) in [True, False]
    assert btcusd.price_above_weekly_SMA(50) in [True, False]

    price = btcusd.get_asset_price()
    assert price > 0
    assert btcusd.price_below_weekly_SMA(50) == (
        price < btcusd.df_1w['sma_50'].iloc[-1])
    assert btcusd.price_above_weekly_SMA(50) == (
        price > btcusd.df_1w['sma_50'].iloc[-1])
