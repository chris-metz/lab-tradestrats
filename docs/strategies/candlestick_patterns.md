# Candlestick Patterns

## Kategorie
Price Action — kein Indikator noetig

## Idee
Klassische japanische Kerzenmuster erkennen und als Kauf-/Verkaufssignale nutzen. Bestimmte Formationen (z.B. Hammer am Tief, Shooting Star am Hoch) deuten auf Reversals hin.

## Logik
- **Buy**: Bullish Engulfing, Hammer, Morning Star, Three White Soldiers
- **Sell**: Bearish Engulfing, Shooting Star, Evening Star, Three Black Crows
- Optional: Nur traden wenn Pattern an Support/Resistance auftritt (Konfluenz)

## Parameter
- `min_body_ratio` — Mindestgroesse des Kerzenkoerpers relativ zur Range
- `confirmation` — Naechste Kerze muss Signal bestaetigen (ja/nein)
- `trend_filter` — Pattern nur in Trendrichtung handeln

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- `pandas-ta` hat `ta.cdl_pattern()` fuer viele Candlestick-Muster
- Alternativ: Eigene Erkennung ueber OHLC-Verhaeltnisse
- Aufwand: **Gering** — 1-2 Stunden

## Varianten
- Einzelne Patterns vs. Kombination mehrerer Patterns
- Mit Volumen-Bestaetigung (hohes Volumen = staerkeres Signal)
- Nur an signifikanten Preisniveaus (z.B. runde Zahlen, vorherige Hochs/Tiefs)
