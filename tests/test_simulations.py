"""Unit tests for simulations route."""

import azure.functions as func
from routes.simulations import get_simulations


def test_get_simulations():
    """Test that get_simulations returns a valid HTTP response."""
    req = func.HttpRequest(method="GET", body=None, url="/api/simulations", params={})

    response = get_simulations(req)

    assert response.status_code == 200
    assert response.mimetype == "text/html"
    assert len(response.get_body()) > 0
