# SMA Crossover

## Kategorie
Indikator-basiert — Trend-Following

## Idee
Klassische Crossover-Strategie mit zwei Simple Moving Averages. Wenn der schnelle SMA den langsamen SMA von unten kreuzt, wird ein Aufwaertstrend signalisiert. Kreuzt er von oben, wird ein Abwaertstrend angenommen.

## Logik
- **Buy**: `sma_fast > sma_slow` (schneller SMA liegt ueber dem langsamen)
- **Sell**: `sma_fast < sma_slow` (schneller SMA liegt unter dem langsamen)
- **Hold**: Waehrend der Warmup-Phase (nicht genug Daten fuer SMAs)

## Parameter
| Parameter | Default | Beschreibung |
|-----------|---------|-------------|
| `fast_period` | 20 | Periode des schnellen SMA |
| `slow_period` | 50 | Periode des langsamen SMA |

## Ausgabe-Spalten
- `sma_fast` — Schneller Simple Moving Average
- `sma_slow` — Langsamer Simple Moving Average
- `signal` — 1 (buy), -1 (sell), 0 (hold)

## Nutzung
```bash
uv run tradestrats backtest -S sma BTC/USDT
```

## Staerken & Schwaechen
- **Staerke**: Einfach, robust, funktioniert gut in starken Trends
- **Schwaeche**: Verzoegerte Signale (lagging), schlecht in Seitwaertsmaerkten (Whipsaws)
