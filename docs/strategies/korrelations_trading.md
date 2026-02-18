# Korrelations-Trading (Crypto vs. TradFi)

## Kategorie
Korrelations-basiert / Makro

## Idee
Crypto korreliert zunehmend mit traditionellen Maerkten. Bekannte Korrelationen:
- **BTC ~ Nasdaq/S&P500**: Seit 2020 oft hohe positive Korrelation
- **BTC ~ DXY (US Dollar Index)**: Oft inverse Korrelation (Dollar stark → BTC schwach)
- **BTC ~ Gold**: Phasenweise positiv (Risk-Off Asset) oder negativ

Wenn die Korrelation stabil ist, koennen Bewegungen im korrelierenden Asset als Fruehindikator fuer Crypto dienen (weil TradFi-Maerkte frueher reagieren).

## Logik

### Variante 1: Lead-Lag
- Wenn S&P500 Futures stark steigen/fallen (Pre-Market), Crypto in gleiche Richtung handeln
- Crypto reagiert oft verzoegert auf TradFi-Moves

### Variante 2: Korrelations-Break
- Wenn die uebliche Korrelation bricht (z.B. BTC steigt waehrend S&P faellt), ist das ein starkes Signal
- Korrelation berechnen (Rolling Window), bei Abweichung handeln

### Variante 3: DXY Inverse
- **Buy BTC**: DXY faellt unter wichtiges Niveau / MA
- **Sell BTC**: DXY bricht nach oben aus

## Parameter
- `correlation_window` — Fenster fuer Rolling Correlation (default: 30 Tage)
- `correlation_threshold` — Ab welcher Korrelation gilt sie als "stabil" (default: 0.7)
- `lead_lag_hours` — Erwartete Verzoegerung zwischen TradFi und Crypto
- `reference_asset` — "SPX", "NDX", "DXY", "GOLD"

## Datenquellen
- **yfinance**: S&P500, Nasdaq, DXY, Gold — kostenlos (`pip install yfinance`)
- **Alpha Vantage**: Aehnlich, mit API-Key (kostenloser Tier)
- **FRED API**: US-Wirtschaftsdaten (DXY, Zinsen) — kostenlos

## Umsetzung
1. Neuer Fetcher fuer TradFi-Daten (yfinance als einfachster Einstieg)
2. Korrelations-Berechnung (Rolling Pearson)
3. Signal-Generierung basierend auf Korrelation + TradFi-Bewegung
- Aufwand: **Mittel bis Hoch** — Multi-Asset-Daten, Zeitzonen-Alignment, Boersenzeiten vs. 24/7

## Herausforderungen
- TradFi handelt nicht 24/7 — Luecken am Wochenende und nachts
- Korrelation ist nicht stabil — wechselt zwischen Phasen
- Backtesting muss unterschiedliche Handelszeiten beruecksichtigen
