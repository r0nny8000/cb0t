"""Ticker-related HTTP routes."""

import logging
import azure.functions as func
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from kraken.spot import Market
from kraken.exceptions import KrakenUnknownAssetError, KrakenUnknownAssetPairError
from utils.html_renderer import html
from utils.data_converter import ohlc_to_dataframe


def get_ticker(req: func.HttpRequest) -> func.HttpResponse:
    """
    HTTP triggered function to handle requests to get the latest ticker information for the Kraken ticker.
    The parameter 'pair' can be provided to specify which asset pairs to retrieve ticker information for.
    """
    pair = req.params.get("pair")

    # Default asset pairs if none are provided
    if not pair:
        pair = "XXBTZEUR"

    logging.debug(f"Ticker function is processing with pair: {pair}")

    try:
        # Fetch ticker and asset pair information from Kraken Market
        ticker = Market().get_ticker(pair)

        # Fetch asset pair details
        assets = Market().get_asset_pairs(pair)

        # Load ohlc data for each asset pair with weekly closing interval
        ohlc = Market().get_ohlc(pair, 10080)

        logging.debug(f"Ticker data: {ticker}")

        # Create candlestick chart from OHLC data
        chart = _create_candlestick_chart(ohlc, pair)

    except (KrakenUnknownAssetError, KrakenUnknownAssetPairError) as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)

    return html(template="ticker.html.j2", pair=pair, ticker=ticker, assets=assets, chart=chart)


def _create_candlestick_chart(ohlc_data: dict, pair: str) -> str:
    """Create interactive candlestick chart from OHLC data using Plotly."""
    fig = go.Figure()

    # Extract OHLC data
    data = []
    for v in ohlc_data.values():
        data = v
        break

    # Convert OHLC data to DataFrame
    df = ohlc_to_dataframe(data)

    # Keep only the latest 365 data points
    df = df.tail(365)

    # Add candlestick trace
    fig.add_trace(go.Candlestick(x=df["time"], open=df["open"], high=df["high"], low=df["low"], close=df["close"], name=pair))

    # Calculate 50 week moving average
    df["sma_50"] = df["close"].rolling(window=50).mean()

    # Add moving average line
    fig.add_trace(go.Scatter(x=df["time"], y=df["sma_50"], mode="lines", name="50 SMA", line=dict(color="orange", width=2)))

    # Update layout
    fig.update_layout(title="Price Chart", xaxis_title="Date", yaxis_title="Price", template="plotly_dark", height=600, xaxis_rangeslider_visible=False)

    return fig.to_html(include_plotlyjs="cdn", div_id="candlestick-chart")
