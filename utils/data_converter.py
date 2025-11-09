"""Utility functions for data conversion and processing."""

import pandas as pd


def ohlc_to_dataframe(ohlc_data: list) -> pd.DataFrame:
    """Convert OHLC data from Kraken API to a pandas DataFrame with datetime index."""
    df = pd.DataFrame(ohlc_data, columns=["time", "open", "high", "low", "close", "vwap", "volume", "count"])
    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df
