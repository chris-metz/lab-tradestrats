# tradestrats

Trading-Strategie-Analyse und Backtesting-Framework fuer Krypto- und Aktienmaerkte.

## Features

- **Datenabruf** — OHLCV-Daten via ccxt (Crypto) und yfinance (Aktien, ETFs, Indizes) mit automatischem Parquet-Caching
- **Strategien** — Flexibles Interface fuer beliebige Strategietypen (SMA Crossover, RSI Mean-Reversion, Bollinger Band Scalping, Box Theory)
- **Backtesting** — Vektorisiertes Backtesting mit vectorbt (Sharpe, Drawdown, Win Rate etc.)
- **Indikatoren** — Zugriff auf 130+ technische Indikatoren via pandas-ta
- **Visualisierung** — Interaktive Plotly-Charts (Candlestick, Equity Curve, Signale)
- **CLI-Backtest** — Backtests direkt aus dem Terminal mit `tradestrats backtest`
- **Dashboard** — Interaktives Streamlit-Dashboard fuer Backtesting im Browser

## Setup

```bash
uv sync --extra dev
```

## CLI

```bash
# Crypto-Daten fetchen (ccxt)
uv run tradestrats fetch BTC/USDT -t 1d -s 2024-01-01 -e 2026-01-01
uv run tradestrats fetch ETH/USDT -t 4h
uv run tradestrats fetch                    # Default: BTC/USDT, 1h, letzte 6 Monate

# Aktien-Daten fetchen (yfinance) — Symbol ohne "/" wird automatisch erkannt
uv run tradestrats fetch AAPL -t 1d -s 2025-01-01
uv run tradestrats fetch MSFT -t 1h
uv run tradestrats fetch ^GSPC -t 1d        # S&P 500 Index

# Cache inspizieren
uv run tradestrats cache                    # Alle gecachten Dateien auflisten
uv run tradestrats cache 1                  # Details + letzte 10 Zeilen
uv run tradestrats cache 1 --head -n 20     # Erste 20 Zeilen anzeigen

# Backtest — Crypto
uv run tradestrats backtest                              # Default: RSI, BTC/USDT, 1d, 6 Monate
uv run tradestrats backtest --strategy sma               # SMA Crossover
uv run tradestrats backtest ETH/USDT --strategy bb -t 5m # Bollinger Band Scalping auf 5m
uv run tradestrats backtest --strategy rsi -t 4h         # RSI auf 4h-Candles

# Backtest — Aktien
uv run tradestrats backtest AAPL -S sma -t 1d            # Apple mit SMA Crossover
uv run tradestrats backtest MSFT -S bb -t 1h             # Microsoft mit Bollinger Bands
uv run tradestrats backtest AAPL -S box -t 5m            # Apple mit Box Theory (5m)

# Allgemeine Optionen
uv run tradestrats backtest -s 2025-01-01 -e 2025-06-01  # Custom Zeitraum
uv run tradestrats backtest --cash 50000 --fees 0.002    # Custom Kapital/Fees
```

### fetch

| Parameter | Beschreibung | Default |
|-----------|-------------|---------|
| `symbol` | Crypto-Pair (`BTC/USDT`) oder Aktien-Ticker (`AAPL`, `^GSPC`) | `BTC/USDT` |
| `-t, --timeframe` | Candle-Groesse: `1m, 5m, 15m, 1h, 4h, 1d` | `1h` |
| `-s, --start` | Startzeitpunkt, z.B. `2025-01-01` | 6 Monate zurueck |
| `-e, --end` | Endzeitpunkt, z.B. `2026-01-01` | jetzt |
| `--exchange` | Boerse (nur Crypto) | `binance` |

### cache

| Parameter | Beschreibung | Default |
|-----------|-------------|---------|
| `file` | Dateinummer oder Name zum Inspizieren | alle auflisten |
| `-n, --rows` | Anzahl Zeilen anzeigen | `10` |
| `--head` | Erste statt letzte Zeilen anzeigen | aus |

### backtest

| Parameter | Beschreibung | Default |
|-----------|-------------|---------|
| `symbol` | Crypto-Pair (`BTC/USDT`) oder Aktien-Ticker (`AAPL`) | `BTC/USDT` |
| `-S, --strategy` | Strategie: `rsi`, `sma`, `bb` oder `box` | `rsi` |
| `-t, --timeframe` | Candle-Groesse: `1m, 5m, 15m, 1h, 4h, 1d` | Strategie-Default |
| `-s, --start` | Startzeitpunkt, z.B. `2025-01-01` | 6 Monate zurueck |
| `-e, --end` | Endzeitpunkt, z.B. `2025-06-01` | jetzt |
| `--exchange` | Boerse (nur Crypto) | `binance` |
| `--cash` | Startkapital | `10000` |
| `--fees` | Fee-Rate (Dezimalzahl, z.B. `0.001` = 0.1%) | `0.001` |
| `--sl` | Stop-Loss (Dezimalzahl, z.B. `0.05` = 5%) | `0.05` |

## Dashboard

Interaktives Streamlit-Dashboard fuer Backtesting im Browser.

```bash
# Streamlit installieren (einmalig)
uv sync --extra dashboard

# Dashboard starten
uv run tradestrats dashboard
```

Im Dashboard koennen Strategie, Markt-Parameter und Portfolio-Einstellungen per UI konfiguriert und Backtests per Klick gestartet werden. Ueber den Crypto/Stocks-Toggle in der Sidebar koennen sowohl Krypto-Paare als auch Aktien-Ticker analysiert werden. Ergebnisse werden als Metriken und interaktive Plotly-Charts angezeigt.

## Quickstart (Python)

```python
from tradestrats.data.fetcher import fetch_ohlcv
from tradestrats.strategies.sma_cross import SMACrossover
from tradestrats.backtesting.engine import run

# Crypto-Daten laden
data = fetch_ohlcv("BTC/USDT", timeframe="1h", start="2025-01-01")

# Oder Aktien-Daten — wird automatisch erkannt
# data = fetch_ohlcv("AAPL", timeframe="1d", start="2025-01-01")

# Strategie + Backtest
result = run(SMACrossover(fast_period=20, slow_period=50), data)
print(result.summary())
```

Notebooks:
- `notebooks/01_getting_started.ipynb` — SMA Crossover Walkthrough
- `notebooks/02_rsi_strategy.ipynb` — RSI Mean-Reversion Strategie

## Projektstruktur

```
src/tradestrats/
├── cli.py                 # CLI (fetch, cache, backtest, dashboard)
├── dashboard.py           # Streamlit Backtesting Dashboard
├── config.py              # Zentrale Konfiguration
├── data/fetcher.py        # Datenabruf (ccxt + yfinance) + Parquet-Caching
├── strategies/
│   ├── base.py            # Abstrakte Strategy-Basisklasse
│   ├── sma_cross.py       # SMA Crossover (Trend-Following)
│   ├── rsi_mean_reversion.py # RSI Mean-Reversion
│   ├── bollinger_band.py  # Bollinger Band Scalping
│   └── box_theory.py      # Box Theory (Intraday Mean-Reversion)
├── backtesting/engine.py  # vectorbt Backtesting Runner
├── indicators/registry.py # pandas-ta Indikator-Wrapper
└── visualization/charts.py # Plotly Charts
```

## Tests

```bash
uv run pytest
```

## Eigene Strategie schreiben

```python
from tradestrats.strategies.base import Strategy
import pandas as pd
import pandas_ta as ta

class MyStrategy(Strategy):
    name = "My Strategy"

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()
        df["rsi"] = ta.rsi(df["close"], length=14)
        df["signal"] = 0
        df.loc[df["rsi"] < 30, "signal"] = 1   # Buy bei ueberverkauft
        df.loc[df["rsi"] > 70, "signal"] = -1  # Sell bei ueberkauft
        return df
```
