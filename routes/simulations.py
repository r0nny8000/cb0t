"""Environment-related HTTP routes."""

import os
import logging
import azure.functions as func
import yfinance as yf
import pandas as pd
from utils.html_renderer import html


def get_simulations(req: func.HttpRequest) -> func.HttpResponse:
    """This function executes different simulations with the simple moving average inverstment approach."""

    # Load Bitcoin USD OHLC data from Yahoo Finance (all-time history with daily timeframes)
    btc_ticker = yf.Ticker("BTC-USD")
    df = btc_ticker.history(period="max", interval="1d")

    # Remove unnecessary columns
    df = df.drop(columns=["Dividends", "Stock Splits"])

    # Trim DataFrame to the last 3560 entries for performance
    df = df.tail(3560)

    # Reset index to make Date a column instead of index
    df = df.reset_index()

    # Calculate 125-day moving average
    df["SMA_125"] = df["Close"].rolling(window=125).mean()

    # Store the size of the dataframe
    dataframe_size = len(df)

    # Print data info to log
    logging.info(f"DataFrame size: {dataframe_size}")
    logging.info(f"DataFrame columns: {df.columns.tolist()}")

    # Iterate over the DataFrame
    for index, row in df.iterrows():
        # Process each row
        if row["Close"] < row["SMA_125"]:
            logging.warning(f"Bearish signal on {row['Date']}: Close {row['Close']} < SMA_125 {row['SMA_125']}")
        else:
            logging.info(f"Bullish signal on {row['Date']}: Close {row['Close']} >= SMA_125 {row['SMA_125']}")
        # Your logic here
        pass

    return html("simulations.html.j2", dataframe=df.tail().to_html(classes="table table-dark table-striped table-hover"))
