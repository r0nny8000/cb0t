from cb0t.btcusd import BTCUSD
import cb0t.engine as engine


def test_get_data():
    btcusd = BTCUSD()
    result = btcusd.get_data()

    assert result is not None
    assert isinstance(result, list)
    assert len(result) == 8
