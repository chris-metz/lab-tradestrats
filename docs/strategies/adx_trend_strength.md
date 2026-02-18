# ADX Trend Strength Filter

## Kategorie
Indikator-basiert — Trendfilter / Meta-Strategie

## Idee
Der ADX (Average Directional Index) misst die Staerke eines Trends, unabhaengig von der Richtung. Idee: Nur handeln wenn ein starker Trend vorliegt, und in Seitwaertsmaerkten flat bleiben. Kann als Standalone oder als Filter fuer andere Strategien genutzt werden.

## Logik
- ADX > 25 = Trend vorhanden, handeln erlaubt
- ADX < 20 = Kein Trend, nicht handeln
- **+DI > -DI** = Aufwaertstrend → Buy
- **-DI > +DI** = Abwaertstrend → Sell
- Optional: ADX steigend = Trend wird staerker (Entry), ADX fallend = Trend wird schwaecher (Exit)

## Parameter
- `adx_period` — ADX-Berechnung (default: 14)
- `trend_threshold` — Ab welchem ADX-Wert ist ein Trend "stark genug" (default: 25)
- `use_di_cross` — DI-Crossover als Signal nutzen (ja/nein)

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- `pandas-ta` hat `ta.adx()` — liefert ADX, +DI, -DI
- Aufwand: **Sehr gering**

## Besonderheit
- Sehr gut als **Kombination mit anderen Strategien**: z.B. RSI nur handeln wenn ADX > 25
- Reduziert Fehlsignale in Ranging-Maerkten erheblich
- Kann als generischer `TrendFilter`-Wrapper implementiert werden
