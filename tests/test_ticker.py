"""Unit tests for ticker route."""

import azure.functions as func
from routes.ticker import get_ticker


def test_get_ticker():
    """Test that get_ticker returns a valid HTTP response."""
    req = func.HttpRequest(method="GET", body=None, url="/api/ticker", params={})

    response = get_ticker(req)

    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert len(response.get_body()) > 0


def test_get_ticker_with_pair():
    """Test that get_ticker works with custom pair parameter."""
    req = func.HttpRequest(method="GET", body=None, url="/api/ticker", params={"pair": "XETHZEUR"})

    response = get_ticker(req)

    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert len(response.get_body()) > 0
