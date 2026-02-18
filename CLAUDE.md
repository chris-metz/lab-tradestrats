# CLAUDE.md — tradestrats

## Projekt

Trading-Strategie-Analyse und Backtesting-Framework fuer Kryptomaerkte. Python 3.12, verwaltet mit uv.

## Commands

- `uv sync --extra dev` — Dependencies installieren
- `uv run pytest` — Tests ausfuehren
- `uv run jupyter notebook` — Jupyter starten
- `uv run tradestrats backtest` — Backtest aus dem Terminal (Default: RSI, BTC/USDT, 1d, 6Mo)
- `uv sync --extra dashboard && uv run tradestrats dashboard` — Streamlit-Dashboard starten

## Architektur

- **src-Layout**: Code liegt in `src/tradestrats/`, installiert als Package
- **Datenfluss**: `fetcher.py` → OHLCV DataFrame → `Strategy.generate_signals()` → `engine.run()` → `BacktestResult`
- **Caching**: OHLCV-Daten werden automatisch als Parquet in `data/` gecacht
- **Strategien**: Erben von `strategies/base.py:Strategy`, muessen `generate_signals(data) -> DataFrame` implementieren. Signal-Spalte: 1=buy, -1=sell, 0=hold. Vorhandene Strategien: `sma_cross.py` (Trend-Following), `rsi_mean_reversion.py` (Mean-Reversion), `bollinger_band.py` (Scalping)

## Konventionen

- Sprache im Code: Englisch (Variablen, Docstrings, Kommentare)
- Sprache in Docs/README: Deutsch
- Type Hints verwenden (`from __future__ import annotations`)
- Neue Strategien in `src/tradestrats/strategies/` anlegen, von `Strategy` erben
- Tests in `tests/`, Prefix `test_`
- Daten-Dateien (Parquet) gehoeren nicht ins Git
- Git-Befehle immer relativ im Projektverzeichnis ausfuehren, keine absoluten Pfade (`git status` statt `git -C /abs/path status`)

## Kern-Dependencies

- **ccxt** — Boersen-API-Abstraktion
- **vectorbt** — Vektorisiertes Backtesting
- **pandas-ta** — Technische Indikatoren
- **plotly** — Interaktive Charts
- **pyarrow** — Parquet I/O
