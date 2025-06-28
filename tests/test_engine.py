import cb0t.engine as engine


def test_get_ohlc():
    result = engine.get_ohlc("BTC/USD", "1m", 5)

    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 5
