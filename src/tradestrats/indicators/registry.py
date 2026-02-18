from __future__ import annotations

import pandas as pd
import pandas_ta as ta


def get_indicator(name: str, data: pd.DataFrame, **params) -> pd.DataFrame | pd.Series:
    """Compute a technical indicator using pandas-ta.

    Args:
        name: Indicator name (e.g. "sma", "rsi", "macd", "bbands").
        data: OHLCV DataFrame with at least a 'close' column.
        **params: Parameters passed to the pandas-ta indicator function.

    Returns:
        Series or DataFrame with the computed indicator values.
    """
    func = getattr(ta, name, None)
    if func is None:
        raise ValueError(f"Unknown indicator: {name!r}. Check pandas_ta docs for available indicators.")

    # Most indicators work on the close price by default
    close = data["close"]
    high = data.get("high")
    low = data.get("low")
    volume = data.get("volume")

    # Indicators that need OHLCV columns
    ohlcv_indicators = {"atr", "adx", "stoch", "supertrend", "ichimoku", "kc", "donchian"}
    hlc_indicators = {"atr", "adx", "stoch", "supertrend", "kc"}

    if name.lower() in hlc_indicators and high is not None and low is not None:
        return func(high=high, low=low, close=close, **params)
    elif name.lower() in {"obv", "ad", "cmf", "mfi", "vwap"} and volume is not None:
        if name.lower() in {"mfi"} and high is not None and low is not None:
            return func(high=high, low=low, close=close, volume=volume, **params)
        return func(close=close, volume=volume, **params)
    else:
        return func(close=close, **params)


def list_indicators() -> list[str]:
    """List all available indicator names from pandas-ta."""
    # pandas-ta registers indicators as functions in the module
    return [name for name in dir(ta) if not name.startswith("_") and callable(getattr(ta, name))]
