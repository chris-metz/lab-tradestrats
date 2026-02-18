"""Smoke tests for the data fetcher module."""

from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from tradestrats.data.fetcher import _cache_path, fetch_ohlcv, is_stock_symbol


# --- Symbol detection ---

def test_is_stock_symbol_crypto():
    """Symbols with '/' are crypto pairs."""
    assert not is_stock_symbol("BTC/USDT")
    assert not is_stock_symbol("ETH/BTC")


def test_is_stock_symbol_stocks():
    """Symbols without '/' are stock tickers."""
    assert is_stock_symbol("AAPL")
    assert is_stock_symbol("MSFT")
    assert is_stock_symbol("^GSPC")


# --- Cache path ---

def test_cache_path_format():
    """Cache path should encode exchange, symbol, and timeframe."""
    path = _cache_path("BTC/USDT", "1h", "binance")
    assert path.name == "binance_BTC_USDT_1h.parquet"


def test_cache_path_stock():
    """Stock symbols get a yfinance-prefixed cache path."""
    path = _cache_path("AAPL", "1d", "binance")
    assert path.name == "yfinance_AAPL_1d.parquet"


def test_cache_path_stock_index():
    """Index symbols with ^ get sanitized in the cache path."""
    path = _cache_path("^GSPC", "1d", "binance")
    assert path.name == "yfinance_IDX_GSPC_1d.parquet"


# --- ccxt fetch ---

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


# --- yfinance fetch ---

def _make_yf_history(rows: int = 3) -> pd.DataFrame:
    """Create a mock yfinance history DataFrame."""
    idx = pd.date_range("2025-01-01", periods=rows, freq="D", tz="America/New_York")
    return pd.DataFrame(
        {
            "Open": [150.0 + i for i in range(rows)],
            "High": [155.0 + i for i in range(rows)],
            "Low": [149.0 + i for i in range(rows)],
            "Close": [152.0 + i for i in range(rows)],
            "Volume": [1_000_000 + i * 100 for i in range(rows)],
            "Dividends": [0.0] * rows,
            "Stock Splits": [0.0] * rows,
        },
        index=idx,
    )


def test_fetch_yfinance_returns_correct_format():
    """yfinance fetch should return DataFrame with correct columns and UTC index."""
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = _make_yf_history()

    with patch("tradestrats.data.fetcher.yf.Ticker", return_value=mock_ticker):
        df = fetch_ohlcv("AAPL", timeframe="1d", start="2025-01-01", use_cache=False)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["open", "high", "low", "close", "volume"]
    assert len(df) == 3
    assert isinstance(df.index, pd.DatetimeIndex)
    assert str(df.index.tz) == "UTC"


def test_fetch_yfinance_unsupported_timeframe():
    """yfinance should raise ValueError for unsupported intervals like 4h."""
    with pytest.raises(ValueError, match="yfinance does not support interval '4h'"):
        fetch_ohlcv("AAPL", timeframe="4h", use_cache=False)


def test_fetch_yfinance_empty_response():
    """yfinance fetch should handle empty history gracefully."""
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = pd.DataFrame()

    with patch("tradestrats.data.fetcher.yf.Ticker", return_value=mock_ticker):
        df = fetch_ohlcv("AAPL", timeframe="1d", start="2025-01-01", use_cache=False)

    assert isinstance(df, pd.DataFrame)
    assert df.empty
