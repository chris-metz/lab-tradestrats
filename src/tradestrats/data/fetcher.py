from __future__ import annotations

from datetime import datetime
from pathlib import Path

import ccxt
import pandas as pd
import yfinance as yf

from tradestrats.config import DATA_DIR, DEFAULT_EXCHANGE, DEFAULT_TIMEFRAME

# yfinance supported intervals (subset we allow)
_YF_INTERVALS = {"1m", "5m", "15m", "1h", "1d"}


def is_stock_symbol(symbol: str) -> bool:
    """Return True if the symbol is a stock/ETF ticker (no '/' → yfinance)."""
    return "/" not in symbol


def _get_exchange(exchange_id: str = DEFAULT_EXCHANGE) -> ccxt.Exchange:
    """Create a ccxt exchange instance."""
    exchange_class = getattr(ccxt, exchange_id)
    return exchange_class({"enableRateLimit": True})


def _cache_path(symbol: str, timeframe: str, exchange_id: str) -> Path:
    """Build the Parquet cache file path for a given symbol/timeframe/exchange."""
    if is_stock_symbol(symbol):
        safe_symbol = symbol.replace("^", "IDX_")
        return DATA_DIR / f"yfinance_{safe_symbol}_{timeframe}.parquet"
    safe_symbol = symbol.replace("/", "_")
    return DATA_DIR / f"{exchange_id}_{safe_symbol}_{timeframe}.parquet"


def _fetch_ohlcv_yfinance(
    symbol: str,
    timeframe: str,
    start: pd.Timestamp | None,
    end: pd.Timestamp | None,
) -> pd.DataFrame:
    """Fetch OHLCV data via yfinance.

    Returns:
        DataFrame with columns: open, high, low, close, volume (UTC DatetimeIndex).
    """
    if timeframe not in _YF_INTERVALS:
        raise ValueError(
            f"yfinance does not support interval '{timeframe}'. "
            f"Supported intervals for stocks: {sorted(_YF_INTERVALS)}"
        )

    ticker = yf.Ticker(symbol)

    # yfinance limits intraday history: 1m/5m/15m → 60 days, 1h → 730 days
    _yf_max_days = {"1m": 59, "5m": 59, "15m": 59, "1h": 729}
    max_days = _yf_max_days.get(timeframe)
    if max_days is not None and start is not None:
        earliest = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=max_days)
        if start < earliest:
            start = earliest

    kwargs: dict = {"interval": timeframe}
    if start is not None:
        kwargs["start"] = start.strftime("%Y-%m-%d")
    if end is not None:
        # yfinance end is exclusive, add one day to include the end date
        kwargs["end"] = (end + pd.Timedelta(days=1)).strftime("%Y-%m-%d")

    # For intraday intervals without a start date, use period-based fetch
    if start is None and timeframe in ("1m", "5m", "15m", "1h"):
        kwargs.pop("start", None)
        kwargs.pop("end", None)
        kwargs["period"] = "60d" if timeframe in ("1m", "5m", "15m") else "730d"

    hist = ticker.history(**kwargs)

    if hist.empty:
        return pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

    # Normalise column names to lowercase
    hist.columns = [c.lower() for c in hist.columns]
    df = hist[["open", "high", "low", "close", "volume"]].copy()

    # Ensure UTC DatetimeIndex
    if df.index.tz is None:
        df.index = df.index.tz_localize("UTC")
    else:
        df.index = df.index.tz_convert("UTC")

    df.index.name = "timestamp"
    return df


def _fetch_ohlcv_ccxt(
    symbol: str,
    timeframe: str,
    fetch_ranges: list[tuple[pd.Timestamp | None, pd.Timestamp]],
    exchange_id: str,
) -> pd.DataFrame:
    """Fetch OHLCV data from a ccxt exchange."""
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

    if all_candles:
        new_df = pd.DataFrame(all_candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
        new_df["timestamp"] = pd.to_datetime(new_df["timestamp"], unit="ms", utc=True)
        new_df = new_df.set_index("timestamp")
    else:
        new_df = pd.DataFrame(columns=["open", "high", "low", "close", "volume"])

    return new_df


def fetch_ohlcv(
    symbol: str,
    timeframe: str = DEFAULT_TIMEFRAME,
    start: str | datetime | None = None,
    end: str | datetime | None = None,
    exchange_id: str = DEFAULT_EXCHANGE,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Fetch OHLCV data with automatic Parquet caching.

    Dispatches to yfinance for stock tickers (no '/') and ccxt for crypto pairs.

    Args:
        symbol: Trading pair ("BTC/USDT") or stock ticker ("AAPL", "^GSPC").
        timeframe: Candle timeframe, e.g. "1h", "4h", "1d".
        start: Start datetime (string or datetime). If None, fetches last 500 candles.
        end: End datetime (string or datetime). If None, fetches up to now.
        exchange_id: Exchange name for ccxt (default: binance). Ignored for stocks.
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

    # --- Dispatch: yfinance (stocks) vs ccxt (crypto) ---
    if is_stock_symbol(symbol):
        new_df = _fetch_ohlcv_yfinance(symbol, timeframe, start_ts, end_ts)
    else:
        new_df = _fetch_ohlcv_ccxt(symbol, timeframe, fetch_ranges, exchange_id)

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
