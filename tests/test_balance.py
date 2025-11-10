"""Unit tests for balance route."""

import os
import pytest
import azure.functions as func
from routes.balance import get_balance


@pytest.mark.skipif(not os.getenv("KRAKENAPIKEY") or not os.getenv("KRAKENAPISECRET"), reason="Kraken API credentials not set")
def test_get_balance():
    """Test that get_balance returns a valid HTTP response."""
    req = func.HttpRequest(method="GET", body=None, url="/api/balance", params={})

    response = get_balance(req)

    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert len(response.get_body()) > 0
