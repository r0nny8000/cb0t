""" imports """
from cb0t.asset_pairs import *  # pylint: disable=wildcard-import,unused-wildcard-import
from cb0t.asset import Asset

btcusd = BTCUSD()

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
    assert btcusd.pair == "XXBTZUSD"

    # force class to calculate the dataframes
    assert btcusd.get_df_1d() is not None
    assert btcusd.get_df_1w() is not None

    assert btcusd.df_1d is not None
    assert btcusd.df_1w is not None

    # check if the dataframes are not empty
    assert len(btcusd.df_1d) > 0
    assert len(btcusd.df_1w) > 0
    assert len(btcusd.df_1d) == 720  # defined my value of kraken
    assert len(btcusd.df_1w) > 610


def test_rsi():
    """
    Test the RSI method of the BTCUSD class.
    """
    # force class to calculate the dataframes
    assert btcusd.get_df_1d() is not None
    assert btcusd.get_df_1w() is not None

    assert 'time' in btcusd.get_df_1d()
    assert 'close' in btcusd.get_df_1d()
    assert 'rsi' not in btcusd.get_df_1d()
    assert btcusd.calculate_rsi() is not None
    assert 'rsi' in btcusd.get_df_1d()
    assert btcusd.get_df_1d()['rsi'].iloc[-1] < 100
    assert btcusd.get_df_1d()['rsi'].iloc[-1] > 0

    assert btcusd.RSI_below(50) in [True, False]
    assert btcusd.RSI_above(50) in [True, False]
    assert btcusd.RSI_below(50) != btcusd.RSI_above(50)

    rsi = btcusd.df_1d['rsi'].iloc[-1]
    assert rsi > 0 and rsi < 100
    assert btcusd.RSI_below(50) == (rsi < 50)
    assert btcusd.RSI_above(50) == (rsi > 50)


def test_sma():
    """
    Test the SMA method of the BTCUSD class.
    """
    # force class to calculate the dataframes
    assert btcusd.get_df_1d() is not None
    assert btcusd.get_df_1w() is not None


    # daily data frame
    assert 'time' in btcusd.get_df_1d()
    assert 'close' in btcusd.get_df_1d()
    assert 'time' in btcusd.get_df_1w()
    assert 'close' in btcusd.get_df_1w()

    assert 'sma_50' not in btcusd.get_df_1d()
    assert 'sma_50' not in btcusd.get_df_1w()
    assert btcusd.calculate_sma(50) is not None
    assert 'sma_50' in btcusd.get_df_1d()
    assert 'sma_50' in btcusd.get_df_1w()

    assert 'sma_200' not in btcusd.get_df_1d()
    assert 'sma_200' not in btcusd.get_df_1w()
    assert btcusd.calculate_sma(200) is not None
    assert 'sma_200' in btcusd.get_df_1d()
    assert 'sma_200' in btcusd.get_df_1w()

    assert btcusd.below_Weekly_SMA(50) in [True, False]
    assert btcusd.above_Weekly_SMA(50) in [True, False]
    assert btcusd.below_Weekly_SMA(50) != btcusd.above_Weekly_SMA(50)

    price = btcusd.get_asset_price()
    assert price > 0
    assert btcusd.below_Weekly_SMA(50) == (price < btcusd.df_1w['sma_50'].iloc[-1])
    assert btcusd.above_Weekly_SMA(50) == (price > btcusd.df_1w['sma_50'].iloc[-1])



def test_get_asset_price():
    """
    Test the get_asset_price method of the BTCUSD class.
    """
    price = btcusd.get_asset_price()
    assert price > 0
    print(f"Current BTC/USD asset price: {price}")

def test_ath():
    """
    Test the ATH method of the BTCUSD class.
    """
    ath = btcusd.get_ath()
    assert ath > 123000  # ATH is above $123,000
    print(f"Current ATH for {btcusd.pair}: {ath}")

def test_accelerate():
    """
    Test the accelerate method of the BTCUSD class.
    """
    amount = 1000.0  # Amount in EUR
    accelerated_amount = btcusd.accelerate(amount)
    assert accelerated_amount >= 1000
    print(f"Accelerated amount for {btcusd.pair}: {accelerated_amount}")