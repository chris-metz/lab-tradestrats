# Trading-Strategien

Dokumentation aller implementierten Strategien. Jede Strategie hat eine eigene Seite mit Beschreibung, Logik, Parametern und Nutzungsbeispielen.

Weitere Strategie-Ideen werden als [GitHub Issues](https://github.com/chris-metz/lab-tradestrats/issues?q=label%3Astrategy-idea) mit dem Label `strategy-idea` verwaltet.

## Implementierte Strategien

| Strategie | Typ | CLI-Key | Timeframe | Stop-Loss | Docs |
|-----------|-----|---------|-----------|-----------|------|
| SMA Crossover | Trend-Following | `sma` | `1d` | 5% | [sma_cross.md](sma_cross.md) |
| RSI Mean Reversion | Mean-Reversion | `rsi` | `1h` | 5% | [rsi_mean_reversion.md](rsi_mean_reversion.md) |
| Bollinger Band Scalping | Scalping | `bb` | `1h` | 3% | [bollinger_band.md](bollinger_band.md) |
| Box Theory | Mean-Reversion (Intraday) | `box` | `5m` | 2% | [box_theory.md](box_theory.md) |

Jede Strategie hat eigene empfohlene Defaults fuer Timeframe und Stop-Loss. Diese werden automatisch in CLI und Dashboard verwendet, wenn nichts anderes angegeben wird. Details in den jeweiligen Docs.

## Schnellstart

```bash
# Backtest mit empfohlenen Strategie-Defaults (Timeframe + Stop-Loss automatisch)
uv run tradestrats backtest -S box BTC/USDT    # → 5m, 2% SL
uv run tradestrats backtest -S sma BTC/USDT    # → 1d, 5% SL

# Manuell ueberschreiben
uv run tradestrats backtest -S box -t 15m --sl 0.03 BTC/USDT
```

## Neue Strategie hinzufuegen

1. Datei in `src/tradestrats/strategies/` anlegen, von `Strategy` erben
2. `generate_signals(data) -> DataFrame` implementieren (Signal-Spalte: 1=buy, -1=sell, 0=hold)
3. In `src/tradestrats/cli.py` importieren und in `STRATEGIES`-Dict eintragen
4. Tests in `tests/test_<name>.py` schreiben
5. Dokumentation hier in `docs/strategies/<name>.md` anlegen
