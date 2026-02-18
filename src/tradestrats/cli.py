from __future__ import annotations

import argparse
from datetime import datetime, timedelta

import pandas as pd

from tradestrats.backtesting import engine
from tradestrats.config import DATA_DIR, DEFAULT_EXCHANGE, DEFAULT_SYMBOL, DEFAULT_TIMEFRAME, TIMEFRAMES
from tradestrats.data.fetcher import fetch_ohlcv
from tradestrats.strategies.bollinger_band import BollingerBandStrategy
from tradestrats.strategies.rsi_mean_reversion import RSIMeanReversion
from tradestrats.strategies.sma_cross import SMACrossover

STRATEGIES = {
    "rsi": lambda: RSIMeanReversion(),
    "sma": lambda: SMACrossover(),
    "bb": lambda: BollingerBandStrategy(),
}


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

    # --- backtest ---
    bt_parser = subparsers.add_parser("backtest", help="Backtest einer Strategie ausfuehren")
    bt_parser.add_argument(
        "symbol",
        nargs="?",
        default=DEFAULT_SYMBOL,
        help=f"Trading-Pair, z.B. BTC/USDT (default: {DEFAULT_SYMBOL})",
    )
    bt_parser.add_argument(
        "-S", "--strategy",
        default="rsi",
        choices=list(STRATEGIES),
        help="Strategie (default: rsi)",
    )
    bt_parser.add_argument(
        "-t", "--timeframe",
        default=DEFAULT_TIMEFRAME,
        choices=TIMEFRAMES,
        help=f"Candle-Groesse (default: {DEFAULT_TIMEFRAME})",
    )
    bt_parser.add_argument(
        "-s", "--start",
        default=None,
        help="Startzeitpunkt, z.B. 2025-01-01 (default: 6 Monate zurueck)",
    )
    bt_parser.add_argument(
        "-e", "--end",
        default=None,
        help="Endzeitpunkt, z.B. 2025-06-01 (default: jetzt)",
    )
    bt_parser.add_argument(
        "--exchange",
        default=DEFAULT_EXCHANGE,
        help=f"Boerse (default: {DEFAULT_EXCHANGE})",
    )
    bt_parser.add_argument(
        "--cash",
        type=float,
        default=10_000.0,
        help="Startkapital (default: 10000)",
    )
    bt_parser.add_argument(
        "--fees",
        type=float,
        default=0.001,
        help="Fee-Rate als Dezimalzahl (default: 0.001 = 0.1%%)",
    )
    bt_parser.add_argument(
        "--sl",
        type=float,
        default=0.05,
        help="Stop-Loss als Dezimalzahl (default: 0.05 = 5%%)",
    )

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    if args.command == "fetch":
        _cmd_fetch(args)
    elif args.command == "cache":
        _cmd_cache(args)
    elif args.command == "backtest":
        _cmd_backtest(args)


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


def _cmd_backtest(args):
    strategy = STRATEGIES[args.strategy]()

    # Default: 6 Monate zurueck
    if args.start is None:
        start = datetime.utcnow() - timedelta(days=180)
    else:
        start = args.start

    end = args.end

    print(f"Strategie:  {strategy.name}")
    print(f"Symbol:     {args.symbol} | {args.timeframe} | {args.exchange}")
    print(f"Zeitraum:   {start} bis {end or 'jetzt'}")
    print(f"Kapital:    {args.cash:,.2f} | Fees: {args.fees} | Stop-Loss: {args.sl:.0%}")
    print()

    print("Lade Daten...")
    data = fetch_ohlcv(
        symbol=args.symbol,
        timeframe=args.timeframe,
        start=start,
        end=end,
        exchange_id=args.exchange,
    )
    print(f"{len(data)} Candles geladen\n")

    print("Starte Backtest...")
    result = engine.run(strategy, data, init_cash=args.cash, fees=args.fees, sl_stop=args.sl)
    print()

    # Summary
    s = result.summary()
    print("=" * 40)
    print("  BACKTEST ERGEBNIS")
    print("=" * 40)
    print(f"  Total Return:  {s['total_return']:>+10.2%}")
    print(f"  Endkapital:    {s['final_value']:>10,.2f}")
    print(f"  Sharpe Ratio:  {s['sharpe_ratio']:>10.2f}")
    print(f"  Max Drawdown:  {s['max_drawdown']:>10.2%}")
    print(f"  Trades:        {s['total_trades']:>10}")
    print(f"  Win Rate:      {s['win_rate']:>10.2%}")
    print("=" * 40)
