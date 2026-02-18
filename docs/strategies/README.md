# Trading-Strategien

Dokumentation aller implementierten Strategien. Jede Strategie hat eine eigene Seite mit Beschreibung, Logik, Parametern und Nutzungsbeispielen.

Weitere Strategie-Ideen werden als [GitHub Issues](https://github.com/chris-metz/lab-tradestrats/issues?q=label%3Astrategy-idea) mit dem Label `strategy-idea` verwaltet.

## Implementierte Strategien

| Strategie | Typ | CLI-Key | Docs | Code |
|-----------|-----|---------|------|------|
| SMA Crossover | Trend-Following | `sma` | [sma_cross.md](sma_cross.md) | [sma_cross.py](../../src/tradestrats/strategies/sma_cross.py) |
| RSI Mean Reversion | Mean-Reversion | `rsi` | [rsi_mean_reversion.md](rsi_mean_reversion.md) | [rsi_mean_reversion.py](../../src/tradestrats/strategies/rsi_mean_reversion.py) |
| Bollinger Band Scalping | Scalping | `bb` | [bollinger_band.md](bollinger_band.md) | [bollinger_band.py](../../src/tradestrats/strategies/bollinger_band.py) |
| Box Theory | Mean-Reversion (Intraday) | `box` | [box_theory.md](box_theory.md) | [box_theory.py](../../src/tradestrats/strategies/box_theory.py) |

## Schnellstart

```bash
# Backtest einer Strategie ausfuehren
uv run tradestrats backtest -S <key> -t <timeframe> <symbol>

# Beispiele
uv run tradestrats backtest -S rsi BTC/USDT              # RSI, 1h, 6 Monate
uv run tradestrats backtest -S box -t 1h --sl 0.02 BTC/USDT  # Box Theory, enger SL
uv run tradestrats backtest -S sma -t 1d ETH/USDT        # SMA, Daily
```

## Neue Strategie hinzufuegen

1. Datei in `src/tradestrats/strategies/` anlegen, von `Strategy` erben
2. `generate_signals(data) -> DataFrame` implementieren (Signal-Spalte: 1=buy, -1=sell, 0=hold)
3. In `src/tradestrats/cli.py` importieren und in `STRATEGIES`-Dict eintragen
4. Tests in `tests/test_<name>.py` schreiben
5. Dokumentation hier in `docs/strategies/<name>.md` anlegen
