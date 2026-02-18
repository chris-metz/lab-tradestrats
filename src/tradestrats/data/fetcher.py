from __future__ import annotations

from datetime import datetime
from pathlib import Path

import ccxt
import pandas as pd

from tradestrats.config import DATA_DIR, DEFAULT_EXCHANGE, DEFAULT_TIMEFRAME


def _get_exchange(exchange_id: str = DEFAULT_EXCHANGE) -> ccxt.Exchange:
    """Create a ccxt exchange instance."""
    exchange_class = getattr(ccxt, exchange_id)
    return exchange_class({"enableRateLimit": True})


def _cache_path(symbol: str, timeframe: str, exchange_id: str) -> Path:
    """Build the Parquet cache file path for a given symbol/timeframe/exchange."""
    safe_symbol = symbol.replace("/", "_")
    return DATA_DIR / f"{exchange_id}_{safe_symbol}_{timeframe}.parquet"


def fetch_ohlcv(
    symbol: str,
    timeframe: str = DEFAULT_TIMEFRAME,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    exchange_id: str = DEFAULT_EXCHANGE,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Fetch OHLCV data via ccxt with automatic Parquet caching.

    Args:
        symbol: Trading pair, e.g. "BTC/USDT".
        timeframe: Candle timeframe, e.g. "1h", "4h", "1d".
        start: Start datetime (string or datetime). If None, fetches last 500 candles.
        end: End datetime (string or datetime). If None, fetches up to now.
        exchange_id: Exchange name for ccxt (default: binance).
        use_cache: If True, read/write Parquet cache.

    Returns:
        DataFrame with columns: open, high, low, close, volume (DatetimeIndex).
    """
    cache_file = _cache_path(symbol, timeframe, exchange_id)

    # Try loading from cache
    if use_cache and cache_file.exists():
        df = pd.read_parquet(cache_file)
        if start is not None:
            start_ts = pd.Timestamp(start, tz="UTC")
            df = df[df.index >= start_ts]
        if end is not None:
            end_ts = pd.Timestamp(end, tz="UTC")
            df = df[df.index <= end_ts]
        if not df.empty:
            return df

    # Fetch from exchange
    exchange = _get_exchange(exchange_id)

    since = None
    if start is not None:
        since = int(pd.Timestamp(start, tz="UTC").timestamp() * 1000)

    end_ms = None
    if end is not None:
        end_ms = int(pd.Timestamp(end, tz="UTC").timestamp() * 1000)

    all_candles: list[list] = []
    limit = 1000  # max candles per request for most exchanges

    while True:
        candles = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
        if not candles:
            break

        all_candles.extend(candles)
        last_ts = candles[-1][0]

        # Stop if we've reached the end
        if end_ms is not None and last_ts >= end_ms:
            break

        # Stop if we got fewer candles than requested (no more data)
        if len(candles) < limit:
            break

        # Move since forward to avoid duplicates
        since = last_ts + 1

    if not all_candles:
        return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

    df = pd.DataFrame(all_candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", utc=True)
    df = df.set_index("timestamp")
    df = df[~df.index.duplicated(keep="last")]
    df = df.sort_index()

    # Filter by end date
    if end_ms is not None:
        end_ts = pd.Timestamp(end, tz="UTC")
        df = df[df.index <= end_ts]

    # Cache to Parquet
    if use_cache:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        # Merge with existing cache if present
        if cache_file.exists():
            existing = pd.read_parquet(cache_file)
            df = pd.concat([existing, df])
            df = df[~df.index.duplicated(keep="last")]
            df = df.sort_index()
        df.to_parquet(cache_file)

    # Apply start/end filters for return value
    if start is not None:
        start_ts = pd.Timestamp(start, tz="UTC")
        df = df[df.index >= start_ts]
    if end is not None:
        end_ts = pd.Timestamp(end, tz="UTC")
        df = df[df.index <= end_ts]

    return df
