# tradestrats

Trading-Strategie-Analyse und Backtesting-Framework fuer Kryptomaerkte.

## Features

- **Datenabruf** — OHLCV-Daten via ccxt (Binance etc.) mit automatischem Parquet-Caching
- **Strategien** — Flexibles Interface fuer beliebige Strategietypen (Beispiel: SMA Crossover)
- **Backtesting** — Vektorisiertes Backtesting mit vectorbt (Sharpe, Drawdown, Win Rate etc.)
- **Indikatoren** — Zugriff auf 130+ technische Indikatoren via pandas-ta
- **Visualisierung** — Interaktive Plotly-Charts (Candlestick, Equity Curve, Signale)

## Setup

```bash
uv sync --extra dev
```

## Quickstart

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

Ausfuehrliches Beispiel: `notebooks/01_getting_started.ipynb`

## Projektstruktur

```
src/tradestrats/
├── config.py              # Zentrale Konfiguration
├── data/fetcher.py        # ccxt Datenabruf + Parquet-Caching
├── strategies/
│   ├── base.py            # Abstrakte Strategy-Basisklasse
│   └── sma_cross.py       # SMA Crossover Beispiel
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
