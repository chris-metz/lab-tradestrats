# RSI Mean Reversion

## Kategorie
Indikator-basiert — Mean-Reversion

## Idee
Der Relative Strength Index (RSI) misst die Staerke von Preisbewegungen auf einer Skala von 0–100. Bei ueberverkauften Werten (< 30) wird ein Ruecksprung erwartet (Buy), bei ueberkauften Werten (> 70) eine Korrektur (Sell).

## Logik
- **Buy**: `RSI < oversold` (Default: RSI < 30)
- **Sell**: `RSI > overbought` (Default: RSI > 70)
- **Hold**: RSI liegt zwischen den Schwellenwerten

## Parameter
| Parameter | Default | Beschreibung |
|-----------|---------|-------------|
| `rsi_period` | 14 | Berechnungsperiode des RSI |
| `oversold` | 30 | Schwellenwert fuer ueberverkauft (Buy) |
| `overbought` | 70 | Schwellenwert fuer ueberkauft (Sell) |

## Ausgabe-Spalten
- `rsi` — RSI-Wert
- `signal` — 1 (buy), -1 (sell), 0 (hold)

## Nutzung
```bash
uv run tradestrats backtest -S rsi BTC/USDT
```

## Staerken & Schwaechen
- **Staerke**: Fruehere Signale als Trend-Following, gut in Range-Maerkten
- **Schwaeche**: Kann in starken Trends zu frueh gegen den Trend handeln
