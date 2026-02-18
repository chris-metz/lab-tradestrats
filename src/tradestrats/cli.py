from __future__ import annotations

import argparse
from datetime import datetime, timedelta

import pandas as pd

from tradestrats.config import DATA_DIR, DEFAULT_EXCHANGE, DEFAULT_SYMBOL, DEFAULT_TIMEFRAME, TIMEFRAMES
from tradestrats.data.fetcher import fetch_ohlcv


def main():
    parser = argparse.ArgumentParser(
        prog="tradestrats",
        description="Trading-Strategie Analyse & Backtesting",
    )
    subparsers = parser.add_subparsers(dest="command")

    # --- fetch ---
    fetch_parser = subparsers.add_parser("fetch", help="OHLCV-Daten von einer Boerse laden")
    fetch_parser.add_argument(
        "symbol",
        nargs="?",
        default=DEFAULT_SYMBOL,
        help=f"Trading-Pair, z.B. BTC/USDT (default: {DEFAULT_SYMBOL})",
    )
    fetch_parser.add_argument(
        "-t", "--timeframe",
        default=DEFAULT_TIMEFRAME,
        choices=TIMEFRAMES,
        help=f"Candle-Groesse (default: {DEFAULT_TIMEFRAME})",
    )
    fetch_parser.add_argument(
        "-s", "--start",
        default=None,
        help="Startzeitpunkt, z.B. 2025-01-01 oder '6 months ago' (default: 6 Monate zurueck)",
    )
    fetch_parser.add_argument(
        "-e", "--end",
        default=None,
        help="Endzeitpunkt, z.B. 2025-06-01 (default: jetzt)",
    )
    fetch_parser.add_argument(
        "--exchange",
        default=DEFAULT_EXCHANGE,
        help=f"Boerse (default: {DEFAULT_EXCHANGE})",
    )

    # --- cache ---
    cache_parser = subparsers.add_parser("cache", help="Gecachte Parquet-Dateien anzeigen")
    cache_parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Dateiname oder Nummer aus der Liste zum Inspizieren",
    )
    cache_parser.add_argument(
        "-n", "--rows",
        type=int,
        default=10,
        help="Anzahl Zeilen anzeigen (default: 10)",
    )
    cache_parser.add_argument(
        "--head",
        action="store_true",
        help="Erste Zeilen statt letzte anzeigen",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "fetch":
        _cmd_fetch(args)
    elif args.command == "cache":
        _cmd_cache(args)


def _cmd_fetch(args):
    # Default: 6 Monate zurueck
    if args.start is None:
        start = datetime.utcnow() - timedelta(days=180)
    else:
        start = args.start

    end = args.end

    print(f"Lade {args.symbol} | {args.timeframe} | {args.exchange}")
    print(f"Zeitraum: {start} bis {end or 'jetzt'}")
    print()

    data = fetch_ohlcv(
        symbol=args.symbol,
        timeframe=args.timeframe,
        start=start,
        end=end,
        exchange_id=args.exchange,
    )

    print(f"{len(data)} Candles geladen\n")
    print(f"Erster Datenpunkt:  {data.index[0]}")
    print(f"Letzter Datenpunkt: {data.index[-1]}")
    print(f"Zeitraum:           {data.index[-1] - data.index[0]}")
    print()

    # Kurzuebersicht
    close = data["close"]
    print(f"Preis aktuell: {close.iloc[-1]:>12,.2f}")
    print(f"Preis min:     {close.min():>12,.2f}")
    print(f"Preis max:     {close.max():>12,.2f}")
    print(f"Volumen total: {data['volume'].sum():>12,.0f}")
    print()
    print("Letzte 5 Candles:")
    print(data.tail().to_string())


def _cmd_cache(args):
    parquet_files = sorted(DATA_DIR.glob("*.parquet"))

    if not parquet_files:
        print("Keine gecachten Dateien gefunden.")
        return

    # List all cached files
    if args.file is None:
        print("Gecachte Dateien:\n")
        for i, f in enumerate(parquet_files, 1):
            df = pd.read_parquet(f)
            size_kb = f.stat().st_size / 1024
            print(f"  [{i}] {f.name}")
            print(f"      {len(df)} Zeilen | {df.index.min()} bis {df.index.max()} | {size_kb:.1f} KB")
            print()
        print(f"Details anzeigen: tradestrats cache <Nr>")
        return

    # Inspect a specific file
    try:
        idx = int(args.file) - 1
        target = parquet_files[idx]
    except (ValueError, IndexError):
        # Try matching by filename
        matches = [f for f in parquet_files if args.file in f.name]
        if not matches:
            print(f"Datei nicht gefunden: {args.file}")
            return
        target = matches[0]

    df = pd.read_parquet(target)
    print(f"Datei: {target.name}")
    print(f"Groesse: {target.stat().st_size / 1024:.1f} KB")
    print(f"Zeilen: {len(df)}")
    print(f"Spalten: {list(df.columns)}")
    print(f"Zeitraum: {df.index.min()} bis {df.index.max()}")
    print(f"Index-Typ: {type(df.index).__name__}")
    print()

    # Stats
    if "close" in df.columns:
        print(f"Close min: {df['close'].min():>12,.2f}")
        print(f"Close max: {df['close'].max():>12,.2f}")
        print(f"Close avg: {df['close'].mean():>12,.2f}")
    print()

    # Show rows
    n = args.rows
    if args.head:
        print(f"Erste {n} Zeilen:")
        print(df.head(n).to_string())
    else:
        print(f"Letzte {n} Zeilen:")
        print(df.tail(n).to_string())
