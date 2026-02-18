"""Smoke tests for the data fetcher module."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from tradestrats.data.fetcher import _cache_path, fetch_ohlcv


def test_cache_path_format():
    """Cache path should encode exchange, symbol, and timeframe."""
    path = _cache_path("BTC/USDT", "1h", "binance")
    assert path.name == "binance_BTC_USDT_1h.parquet"


def test_fetch_ohlcv_returns_dataframe():
    """fetch_ohlcv should return a DataFrame with expected columns."""
    mock_candles = [
        [1700000000000, 35000.0, 35500.0, 34800.0, 35200.0, 100.0],
        [1700003600000, 35200.0, 35600.0, 35100.0, 35400.0, 120.0],
        [1700007200000, 35400.0, 35800.0, 35300.0, 35700.0, 110.0],
    ]

    mock_exchange = MagicMock()
    mock_exchange.fetch_ohlcv.return_value = mock_candles

    with patch("tradestrats.data.fetcher._get_exchange", return_value=mock_exchange):
        df = fetch_ohlcv("BTC/USDT", timeframe="1h", use_cache=False)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 3
    assert isinstance(df.index, pd.DatetimeIndex)


def test_fetch_ohlcv_empty_response():
    """fetch_ohlcv should handle empty exchange response gracefully."""
    mock_exchange = MagicMock()
    mock_exchange.fetch_ohlcv.return_value = []

    with patch("tradestrats.data.fetcher._get_exchange", return_value=mock_exchange):
        df = fetch_ohlcv("BTC/USDT", timeframe="1h", use_cache=False)

    assert isinstance(df, pd.DataFrame)
    assert df.empty
