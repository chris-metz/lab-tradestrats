# EMA Ribbon

## Kategorie
Indikator-basiert — Trend-Following

## Idee
Ein "Band" aus mehreren EMAs unterschiedlicher Laenge. Wenn alle EMAs geordnet sind (kuerzeste oben, laengste unten) = starker Trend. Wenn sie sich verflechten = kein Trend. Handeln wenn das Ribbon sich entfaltet.

## Logik
- Berechne z.B. 8 EMAs: 8, 13, 21, 34, 55, 89, 144, 233 (Fibonacci)
- **Buy**: Alle EMAs ordnen sich bullish (kuerzeste > laengste) + Preis ueber allen
- **Sell**: Alle EMAs ordnen sich bearish (kuerzeste < laengste) + Preis unter allen
- **Exit**: EMAs beginnen sich zu verflechten (Trend verliert Kraft)

## Parameter
- `ema_lengths` — Liste der EMA-Perioden (default: Fibonacci-Sequenz)
- `min_aligned` — Wieviele EMAs muessen geordnet sein fuer ein Signal (z.B. 6 von 8)
- `price_above_all` — Preis muss ueber/unter allen EMAs sein (ja/nein)

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- Schleife ueber EMA-Laengen, `ta.ema()` fuer jede
- Sortierung pruefen
- Aufwand: **Gering**

## Staerken
- Sehr guter visueller Trendfilter
- Funktioniert auf allen Timeframes
- Faengt grosse Trends frueh ein

## Schwaechen
- Viele Fehlsignale in Seitwaertsmaerkten
- Spaeter Einstieg (EMAs brauchen Zeit sich zu ordnen)
