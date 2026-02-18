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

    start_ts = pd.Timestamp(start, tz="UTC") if start is not None else None
    end_ts = pd.Timestamp(end, tz="UTC") if end is not None else pd.Timestamp.now(tz="UTC")

    # Check cache and determine what we still need to fetch
    cached_df = None
    fetch_ranges: list[tuple[pd.Timestamp | None, pd.Timestamp]] = []

    if use_cache and cache_file.exists():
        cached_df = pd.read_parquet(cache_file)
        cache_start = cached_df.index.min()
        cache_end = cached_df.index.max()

        # Check if we need data before the cache
        if start_ts is not None and start_ts < cache_start:
            fetch_ranges.append((start_ts, cache_start))

        # Check if we need data after the cache
        if end_ts > cache_end:
            fetch_ranges.append((cache_end, end_ts))

        # If cache fully covers the requested range, return from cache
        if not fetch_ranges:
            df = cached_df
            if start_ts is not None:
                df = df[df.index >= start_ts]
            df = df[df.index <= end_ts]
            return df
    else:
        # No cache — fetch everything
        fetch_ranges.append((start_ts, end_ts))

    # Fetch missing ranges from exchange
    exchange = _get_exchange(exchange_id)
    all_candles: list[list] = []
    limit = 1000  # max candles per request for most exchanges

    for range_start, range_end in fetch_ranges:
        since = int(range_start.timestamp() * 1000) if range_start is not None else None
        end_ms = int(range_end.timestamp() * 1000)

        while True:
            candles = exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
            if not candles:
                break

            all_candles.extend(candles)
            last_ts = candles[-1][0]

            # Stop if we've reached the end
            if last_ts >= end_ms:
                break

            # Stop if we got fewer candles than requested (no more data)
            if len(candles) < limit:
                break

            # Move since forward to avoid duplicates
            since = last_ts + 1

    # Build DataFrame from freshly fetched candles
    if all_candles:
        new_df = pd.DataFrame(all_candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        new_df["timestamp"] = pd.to_datetime(new_df["timestamp"], unit="ms", utc=True)
        new_df = new_df.set_index("timestamp")
    else:
        new_df = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

    # Merge with cached data
    if cached_df is not None:
        df = pd.concat([cached_df, new_df])
    else:
        df = new_df

    df = df[~df.index.duplicated(keep="last")]
    df = df.sort_index()

    if df.empty:
        return df

    # Update cache with full dataset
    if use_cache:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        df.to_parquet(cache_file)

    # Apply start/end filters for return value
    if start_ts is not None:
        df = df[df.index >= start_ts]
    df = df[df.index <= end_ts]

    return df
