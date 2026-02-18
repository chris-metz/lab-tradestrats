# Stochastic RSI

## Kategorie
Indikator-basiert — Momentum / Mean-Reversion

## Idee
Der Stochastic RSI wendet den Stochastic-Oszillator auf den RSI an, statt auf den Preis. Das Ergebnis ist ein sehr sensitiver Indikator, der frueher Signale gibt als der normale RSI — aber auch mehr Fehlsignale.

## Logik
- **Buy**: StochRSI %K kreuzt %D von unten in der ueberverkauften Zone (< 20)
- **Sell**: StochRSI %K kreuzt %D von oben in der ueberkauften Zone (> 80)
- Trendfilter empfohlen (z.B. nur Long ueber 200 EMA)

## Parameter
- `rsi_period` — RSI-Berechnung (default: 14)
- `stoch_period` — Stochastic-Fenster (default: 14)
- `k_smooth` — %K Glaettung (default: 3)
- `d_smooth` — %D Glaettung (default: 3)
- `oversold` / `overbought` — Schwellenwerte (default: 20/80)

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- `pandas-ta` hat `ta.stochrsi()` — direkt verfuegbar
- Aufwand: **Sehr gering**

## Vergleich zu normalem RSI
- Sensitiver (mehr Signale, schnellere Reaktion)
- Mehr Fehlsignale in Seitwaertsmaerkten
- Besser fuer kurzfristige Timeframes
