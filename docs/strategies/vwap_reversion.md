# VWAP Reversion

## Kategorie
Indikator-basiert — Intraday Mean-Reversion

## Idee
Der VWAP (Volume Weighted Average Price) ist der volumengewichtete Durchschnittspreis und gilt als "fairer Preis" des Tages. Institutionelle Haendler nutzen ihn als Benchmark. Preis tendiert dazu, zum VWAP zurueckzukehren.

## Logik
- **Buy**: Preis faellt unter VWAP - X Standardabweichungen (ueberverkauft relativ zum VWAP)
- **Sell**: Preis steigt ueber VWAP + X Standardabweichungen (ueberkauft relativ zum VWAP)
- Alternativ: VWAP als Trendfilter (Long nur ueber VWAP, Short nur unter VWAP)

## Parameter
- `std_dev_bands` — Anzahl Standardabweichungen fuer Entry (default: 2.0)
- `anchor` — VWAP-Anker: "session" (taeglich), "weekly", "monthly"
- `mean_reversion` — True = zurueck zum VWAP handeln, False = Breakout vom VWAP

## Datenquellen
OHLCV — bereits vorhanden (Berechnung aus Preis + Volumen)

## Umsetzung
- `pandas-ta` hat `ta.vwap()` — direkt verfuegbar
- Standard-Deviation-Bands muessen manuell berechnet werden
- Aufwand: **Gering**

## Hinweis
- Primaer eine Intraday-Strategie (1m, 5m, 15m)
- VWAP resettet taeglich — auf Tages-/Wochencharts weniger sinnvoll
- Bei Crypto: "Session" kann als UTC-Tag definiert werden
