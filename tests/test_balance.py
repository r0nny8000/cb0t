"""Unit tests for balance route."""

import azure.functions as func
from routes.balance import get_balance


def test_get_balance():
    """Test that get_balance returns a valid HTTP response."""
    req = func.HttpRequest(method="GET", body=None, url="/api/balance", params={})

    response = get_balance(req)

    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert len(response.get_body()) > 0
