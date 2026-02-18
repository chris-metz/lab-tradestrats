# tradestrats

Trading-Strategie-Analyse und Backtesting-Framework fuer Kryptomaerkte.

## Features

- **Datenabruf** — OHLCV-Daten via ccxt (Binance etc.) mit automatischem Parquet-Caching
- **Strategien** — Flexibles Interface fuer beliebige Strategietypen (SMA Crossover, RSI Mean-Reversion)
- **Backtesting** — Vektorisiertes Backtesting mit vectorbt (Sharpe, Drawdown, Win Rate etc.)
- **Indikatoren** — Zugriff auf 130+ technische Indikatoren via pandas-ta
- **Visualisierung** — Interaktive Plotly-Charts (Candlestick, Equity Curve, Signale)
- **CLI-Backtest** — Backtests direkt aus dem Terminal mit `tradestrats backtest`

## Setup

```bash
uv sync --extra dev
```

## CLI

```bash
# Daten fetchen (mit automatischem Parquet-Caching)
uv run tradestrats fetch BTC/USDT -t 1d -s 2024-01-01 -e 2026-01-01
uv run tradestrats fetch ETH/USDT -t 4h
uv run tradestrats fetch                    # Default: BTC/USDT, 1h, letzte 6 Monate

# Cache inspizieren
uv run tradestrats cache                    # Alle gecachten Dateien auflisten
uv run tradestrats cache 1                  # Details + letzte 10 Zeilen
uv run tradestrats cache 1 --head -n 20     # Erste 20 Zeilen anzeigen

# Backtest ausfuehren
uv run tradestrats backtest                              # Default: RSI, BTC/USDT, 1d, 6 Monate
uv run tradestrats backtest --strategy sma               # SMA Crossover
uv run tradestrats backtest --strategy rsi -t 4h         # RSI auf 4h-Candles
uv run tradestrats backtest -s 2025-01-01 -e 2025-06-01  # Custom Zeitraum
uv run tradestrats backtest --cash 50000 --fees 0.002    # Custom Kapital/Fees
```

### fetch

| Parameter | Beschreibung | Default |
|-----------|-------------|---------|
| `symbol` | Trading-Pair, z.B. `BTC/USDT` | `BTC/USDT` |
| `-t, --timeframe` | Candle-Groesse: `1m, 5m, 15m, 1h, 4h, 1d` | `1h` |
| `-s, --start` | Startzeitpunkt, z.B. `2025-01-01` | 6 Monate zurueck |
| `-e, --end` | Endzeitpunkt, z.B. `2026-01-01` | jetzt |
| `--exchange` | Boerse | `binance` |

### cache

| Parameter | Beschreibung | Default |
|-----------|-------------|---------|
| `file` | Dateinummer oder Name zum Inspizieren | alle auflisten |
| `-n, --rows` | Anzahl Zeilen anzeigen | `10` |
| `--head` | Erste statt letzte Zeilen anzeigen | aus |

### backtest

| Parameter | Beschreibung | Default |
|-----------|-------------|---------|
| `symbol` | Trading-Pair, z.B. `BTC/USDT` | `BTC/USDT` |
| `-S, --strategy` | Strategie: `rsi` oder `sma` | `rsi` |
| `-t, --timeframe` | Candle-Groesse: `1m, 5m, 15m, 1h, 4h, 1d` | `1d` |
| `-s, --start` | Startzeitpunkt, z.B. `2025-01-01` | 6 Monate zurueck |
| `-e, --end` | Endzeitpunkt, z.B. `2025-06-01` | jetzt |
| `--exchange` | Boerse | `binance` |
| `--cash` | Startkapital | `10000` |
| `--fees` | Fee-Rate (Dezimalzahl, z.B. `0.001` = 0.1%) | `0.001` |

## Quickstart (Python)

```python
from tradestrats.data.fetcher import fetch_ohlcv
from tradestrats.strategies.sma_cross import SMACrossover
from tradestrats.backtesting.engine import run

# Daten laden
data = fetch_ohlcv("BTC/USDT", timeframe="1h", start="2025-01-01")

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
├── cli.py                 # CLI (fetch, cache, backtest)
├── config.py              # Zentrale Konfiguration
├── data/fetcher.py        # ccxt Datenabruf + Parquet-Caching
├── strategies/
│   ├── base.py            # Abstrakte Strategy-Basisklasse
│   ├── sma_cross.py       # SMA Crossover (Trend-Following)
│   └── rsi_mean_reversion.py # RSI Mean-Reversion
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
