# CLAUDE.md — tradestrats

## Projekt

Trading-Strategie-Analyse und Backtesting-Framework fuer Kryptomaerkte. Python 3.12, verwaltet mit uv.

## Commands

- `uv sync --extra dev` — Dependencies installieren
- `uv run pytest` — Tests ausfuehren
- `uv run jupyter notebook` — Jupyter starten
- `uv run tradestrats backtest` — Backtest aus dem Terminal (Defaults kommen von der Strategie)
- `uv sync --extra dashboard && uv run tradestrats dashboard` — Streamlit-Dashboard starten

## Architektur

- **src-Layout**: Code liegt in `src/tradestrats/`, installiert als Package
- **Datenfluss**: `fetcher.py` → OHLCV DataFrame → `Strategy.generate_signals()` → `engine.run()` → `BacktestResult`
- **Caching**: OHLCV-Daten werden automatisch als Parquet in `data/` gecacht
- **Strategien**: Erben von `strategies/base.py:Strategy`, muessen `generate_signals(data) -> DataFrame` implementieren. Signal-Spalte: 1=buy, -1=sell, 0=hold. Jede Strategie definiert `recommended_timeframe` und `recommended_sl_stop` als Class-Attribute — CLI und Dashboard nutzen diese automatisch.
- **Vorhandene Strategien**: `sma_cross.py` (Trend-Following, 1d, 5% SL), `rsi_mean_reversion.py` (Mean-Reversion, 1h, 5% SL), `bollinger_band.py` (Scalping, 1h, 3% SL), `box_theory.py` (Intraday Mean-Reversion, 5m, 2% SL)
- **Strategie-Docs**: `docs/strategies/<name>.md` — jede implementierte Strategie hat eine eigene Doku-Seite
- **Strategie-Ideen**: 22 Ideen als GitHub Issues mit Label `strategy-idea` verwaltet

## Konventionen

- Sprache im Code: Englisch (Variablen, Docstrings, Kommentare)
- Sprache in Docs/README: Deutsch
- Type Hints verwenden (`from __future__ import annotations`)
- Neue Strategien in `src/tradestrats/strategies/` anlegen, von `Strategy` erben
- Tests in `tests/`, Prefix `test_`
- Daten-Dateien (Parquet) gehoeren nicht ins Git
- Git-Befehle immer relativ im Projektverzeichnis ausfuehren, keine absoluten Pfade (`git status` statt `git -C /abs/path status`)

## Neue Strategie hinzufuegen — Checkliste

1. Code: `src/tradestrats/strategies/<name>.py` — von `Strategy` erben, `recommended_timeframe` + `recommended_sl_stop` setzen
2. CLI: In `cli.py` importieren und in `STRATEGIES`-Dict eintragen
3. Dashboard: In `dashboard.py` importieren, zu `STRATEGY_KEYS` + `_STRATEGY_CLASSES` hinzufuegen, Parameter-UI + `_build_strategy` + `_get_indicators` erweitern
4. Tests: `tests/test_<name>.py`
5. Docs: `docs/strategies/<name>.md` mit Sektionen: Kategorie, Idee, Logik, Parameter, Ausgabe-Spalten, Empfohlene Einstellungen (Defaults), Geeignete Maerkte, Nutzung, Quelle
6. `docs/strategies/README.md` Uebersichtstabelle aktualisieren

## Video-zu-Strategie Workflow

Wenn eine Strategie aus einem YouTube-Video implementiert wird:
1. Transkript lesen fuer die Strategie-Logik
2. ffmpeg nutzen um Frames an relevanten Timestamps zu extrahieren (Charts, Regeln, Live-Trades)
3. Transkript + Frames kombinieren fuer volles Verstaendnis
4. Video-URL in der Strategie-Doku verlinken (Quelle-Sektion)

## Kern-Dependencies

- **ccxt** — Boersen-API-Abstraktion
- **vectorbt** — Vektorisiertes Backtesting
- **pandas-ta** — Technische Indikatoren
- **plotly** — Interaktive Charts
- **pyarrow** — Parquet I/O
