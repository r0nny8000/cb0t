"""Tests for the cost basis calculation service."""

import pytest
from unittest.mock import Mock, patch
from assets.asset import Asset
from kraken.exceptions import KrakenUnknownAssetError
from services.cost_basis import calculate_cost_basis


@pytest.fixture
def mock_asset():
    """Creates a mock asset for testing."""
    asset = Mock(spec=Asset)
    asset.pair = "XXBTZEUR"
    return asset


@pytest.fixture
def three_buy_trades():
    """Test data with 3 different buy trades with 1% fees."""
    return {
        "trades": {
            "trade1": {
                "pair": "XXBTZEUR",
                "type": "buy",
                "vol": "1.0",
                "cost": "45000.0",
                "fee": "450.0"  # 1% of 45000
            },
            "trade2": {
                "pair": "XXBTZEUR",
                "type": "buy",
                "vol": "0.5",
                "cost": "20000.0",
                "fee": "200.0"  # 1% of 20000
            },
            "trade3": {
                "pair": "XXBTZEUR",
                "type": "buy",
                "vol": "0.8",
                "cost": "32000.0",
                "fee": "320.0"  # 1% of 32000
            }
        }
    }


@pytest.fixture
def trades_with_sell():
    """Test data with buy trades and one sell trade with 1% fees."""
    return {
        "trades": {
            "trade1": {
                "pair": "XXBTZEUR",
                "type": "buy",
                "vol": "2.0",
                "cost": "80000.0",
                "fee": "800.0"  # 1% of 80000
            },
            "trade2": {
                "pair": "XXBTZEUR",
                "type": "sell",
                "vol": "0.5",
                "cost": "25000.0",
                "fee": "250.0"  # 1% of 25000
            },
            "trade3": {
                "pair": "XXBTZEUR",
                "type": "buy",
                "vol": "1.5",
                "cost": "60000.0",
                "fee": "600.0"  # 1% of 60000
            }
        }
    }


@patch('services.cost_basis.user')
def test_calculate_cost_basis_three_buy_trades(mock_user, mock_asset, three_buy_trades):
    """Test cost basis calculation with 3 different buy trades."""
    mock_user.get_trades_history.return_value = three_buy_trades

    # Test for amount that requires all three buy trades (1.0 + 0.5 + 0.8 = 2.3)
    result = calculate_cost_basis(mock_asset, 2.0)

    # Expected calculation with 1% fees:
    # Trade1: 1.0 BTC at 45000.0 + 450.0 fee = 45450.0, counter = 2.0 - 1.0 = 1.0
    # Trade2: 0.5 BTC at 20000.0 + 200.0 fee = 20200.0, counter = 1.0 - 0.5 = 0.5
    # Trade3: 0.8 BTC at 32000.0 + 320.0 fee = 32320.0, counter = 0.5 - 0.8 = -0.3 (breaks)
    # Split last trade: 32320.0 * 0.5 / 0.8 = 20200.0
    # Total cost basis: 45450.0 + 20200.0 + 20200.0 = 85850.0
    # Add 0.4% sell fee: 85850.0 * 1.004 = 86193.4
    expected = 86193.4

    assert result == expected
    mock_user.get_trades_history.assert_called_once_with(ofs=0)


@patch('services.cost_basis.user')
def test_calculate_cost_basis_with_sell_trade(mock_user, mock_asset, trades_with_sell):
    """Test cost basis calculation including a sell trade."""
    mock_user.get_trades_history.return_value = trades_with_sell

    # Test for amount that goes through buy, sell, and another buy
    result = calculate_cost_basis(mock_asset, 2.5)

    # Expected calculation with 1% fees:
    # Trade1: Buy 2.0 BTC at 80000.0 + 800.0 fee = 80800.0, counter = 2.5 - 2.0 = 0.5
    # Trade2: Sell 0.5 BTC at 25000.0 (no fee added for sells), counter = 0.5 + 0.5 = 1.0, cost_basis = 80800.0 - 25000.0 = 55800.0
    # Trade3: Buy 1.5 BTC but we only need 1.0, so split: (60000.0 + 600.0) * 1.0 / 1.5 = 60600.0 * 0.6667 = 40400.0
    # Total cost basis: 55800.0 + 40400.0 = 96200.0
    # Add 0.4% sell fee: 96200.0 * 1.004 = 96584.8
    expected = 96584.8

    assert result == expected
    mock_user.get_trades_history.assert_called_once_with(ofs=0)


@patch('services.cost_basis.user')
def test_calculate_cost_basis_partial_buy_trades(mock_user, mock_asset, three_buy_trades):
    """Test cost basis calculation with partial buy trades (amount less than all trades)."""
    mock_user.get_trades_history.return_value = three_buy_trades

    # Test for amount that only requires first two trades
    result = calculate_cost_basis(mock_asset, 1.2)

    # Expected calculation with 1% fees:
    # Trade1: 1.0 BTC at 45000.0 + 450.0 fee = 45450.0, counter = 1.2 - 1.0 = 0.2
    # Trade2: 0.5 BTC but we only need 0.2, so split: (20000.0 + 200.0) * 0.2 / 0.5 = 20200.0 * 0.4 = 8080.0
    # Total cost basis: 45450.0 + 8080.0 = 53530.0
    # Add 0.4% sell fee: 53530.0 * 1.004 = 53744.12
    expected = 53744.12

    assert result == expected


@patch('services.cost_basis.user')
def test_calculate_cost_basis_single_buy_trade(mock_user, mock_asset, three_buy_trades):
    """Test cost basis calculation with only first trade needed."""
    mock_user.get_trades_history.return_value = three_buy_trades

    # Test for amount smaller than first trade volume
    result = calculate_cost_basis(mock_asset, 0.7)

    # Expected calculation with 1% fees:
    # Trade1: 1.0 BTC but we only need 0.7, so split: (45000.0 + 450.0) * 0.7 / 1.0 = 45450.0 * 0.7 = 31815.0
    # Total cost basis: 31815.0
    # Add 0.4% sell fee: 31815.0 * 1.004 = 31942.26
    expected = 31942.26

    assert result == expected


@patch('services.cost_basis.user')
@patch('services.cost_basis.logging')
def test_calculate_cost_basis_api_error(mock_logging, mock_user, mock_asset):
    """Test cost basis calculation when API throws an error."""
    mock_user.get_trades_history.side_effect = KrakenUnknownAssetError("Test error")

    result = calculate_cost_basis(mock_asset, 1.0)

    assert result is None
    mock_logging.error.assert_called_once_with("The asset is unknown.\nDetails: Test error")


@patch('services.cost_basis.user')
def test_calculate_cost_basis_no_trades(mock_user, mock_asset):
    """Test cost basis calculation when no trades are found."""
    mock_user.get_trades_history.return_value = {"trades": {}}

    result = calculate_cost_basis(mock_asset, 1.0)

    # Expected: 0.0 cost basis when no trades exist
    # Add 0.4% sell fee: 0.0 * 1.004 = 0.0
    expected = 0.0

    assert result == expected
