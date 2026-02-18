# OBV Divergenz

## Kategorie
Volumen-basiert — Divergenz

## Idee
On-Balance Volume (OBV) addiert Volumen bei gruenen Kerzen und subtrahiert es bei roten. Wenn der Preis neue Hochs macht aber OBV nicht (oder umgekehrt), ist das eine Divergenz — ein fruehes Warnsignal fuer eine Trendwende.

## Logik
- Berechne OBV (laufende Summe: +Vol bei Up-Kerzen, -Vol bei Down-Kerzen)
- **Bearish Divergenz**: Preis macht hoeheres Hoch, OBV macht tieferes Hoch → Sell
- **Bullish Divergenz**: Preis macht tieferes Tief, OBV macht hoeheres Tief → Buy
- Optional: OBV-Trendlinie oder OBV-MA als zusaetzlicher Filter

## Parameter
- `lookback` — Fenster fuer Divergenz-Erkennung (default: 14)
- `divergence_bars` — Mindestanzahl Kerzen zwischen den Vergleichspunkten
- `obv_ma_period` — Optionaler Moving Average auf OBV fuer Glaettung

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- `pandas-ta` hat `ta.obv()` — eine Zeile
- Divergenz-Erkennung: Swing Highs/Lows vergleichen zwischen Preis und OBV
- Aufwand: **Mittel** — OBV ist trivial, Divergenz-Erkennung braucht etwas Logik

## Staerken
- Fuehrendes Signal (kommt vor der Preisbewegung)
- Funktioniert in allen Maerkten und Timeframes
- Volumen luegt seltener als der Preis
