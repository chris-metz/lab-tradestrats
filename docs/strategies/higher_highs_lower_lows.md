# Higher Highs / Lower Lows (Marktstruktur)

## Kategorie
Price Action — Strukturbasiert

## Idee
Die grundlegendste Form der Trendanalyse: Ein Aufwaertstrend besteht aus hoeheren Hochs (HH) und hoeheren Tiefs (HL). Ein Abwaertstrend aus tieferen Tiefs (LL) und tieferen Hochs (LH). Trendbruch = Signal.

## Logik
- Identifiziere Swing Highs und Swing Lows
- **Buy**: Erster Higher Low nach einer Serie von Lower Lows (Trendwende)
- **Sell**: Erster Lower High nach einer Serie von Higher Highs
- Oder: In Trendrichtung handeln (Buy bei jedem HL im Aufwaertstrend)

## Parameter
- `swing_lookback` — Fenster fuer Swing-Punkt-Erkennung (z.B. 5-10 Kerzen)
- `min_swings` — Mindestanzahl Swings fuer Trenderkennung
- `mode` — "reversal" (Trendwende handeln) oder "continuation" (mit dem Trend)

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- Rolling-Window Swing Detection
- Vergleich aufeinanderfolgender Swing-Punkte
- Aufwand: **Mittel** — saubere Swing-Erkennung braucht Feintuning

## Bezug zu
- Smart Money Concepts (Break of Structure)
- Dow Theory (Trend Definition)
- Elliott Wave (vereinfacht)
