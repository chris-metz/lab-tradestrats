# Funding Rate Strategie

## Kategorie
Sentiment / Derivate-basiert

## Idee
Perpetual Futures haben keinen Verfallstag. Um den Preis am Spot-Preis zu halten, gibt es die Funding Rate: Longs zahlen Shorts (positive Rate) oder Shorts zahlen Longs (negative Rate). Extreme Funding Rates deuten auf uebertriebene Positionierung hin.

## Logik
- **Buy**: Funding Rate extrem negativ (zu viele Shorts → Short Squeeze wahrscheinlich)
- **Sell**: Funding Rate extrem positiv (zu viele Longs → Liquidation wahrscheinlich)
- Optional: Funding Rate Trend (steigend vs. fallend) als Momentum-Signal

## Parameter
- `funding_threshold_long` — Negativer Schwellenwert fuer Buy (z.B. -0.01%)
- `funding_threshold_short` — Positiver Schwellenwert fuer Sell (z.B. +0.03%)
- `lookback_periods` — Anzahl Funding-Perioden fuer Durchschnitt
- `use_trend` — Funding-Rate-Trend als zusaetzliches Signal

## Datenquellen
- **ccxt**: `exchange.fetch_funding_rate_history()` — bereits ueber ccxt verfuegbar
- Binance, Bybit, OKX liefern historische Funding Rates
- Funding wird alle 8 Stunden abgerechnet (3x taeglich)

## Umsetzung
1. Neuer Fetcher fuer Funding Rate History via ccxt
2. Merge mit OHLCV auf 8h-Intervalle (oder Tages-Durchschnitt)
3. Strategie: Threshold-basiert auf Funding Rate
- Aufwand: **Mittel** — ccxt hat die API, aber Daten-Alignment braucht Arbeit

## Vorteile
- Daten kostenlos ueber ccxt
- Nachweislich starker Contrarian-Indikator
- Funktioniert besonders gut bei BTC und ETH

## Einschraenkungen
- Nur fuer Assets mit Perpetual Futures verfuegbar
- Historische Daten oft nur 3-6 Monate zurueck
- 8h-Granularitaet ist relativ grob
