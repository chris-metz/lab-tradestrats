# Support/Resistance Breakout

## Kategorie
Price Action

## Idee
Horizontale Unterstuetzungs- und Widerstandszonen identifizieren. Wenn der Preis eine Zone durchbricht, in Ausbruchsrichtung handeln.

## Logik
- Identifiziere Zonen wo der Preis mehrfach abgeprallt ist (Swing Highs/Lows)
- **Buy**: Close bricht ueber Widerstand mit erhoehtem Volumen
- **Sell**: Close bricht unter Unterstuetzung mit erhoehtem Volumen
- Stop-Loss: Knapp unter/ueber der durchbrochenen Zone (wird zum neuen Support/Resistance)

## Parameter
- `lookback` — Fenster fuer Swing-High/Low-Erkennung (z.B. 20 Kerzen)
- `num_touches` — Mindestanzahl Beruehrungen fuer gueltige Zone
- `zone_tolerance` — Prozentuale Toleranz fuer "gleicher Preis" (z.B. 0.5%)
- `volume_factor` — Um wieviel das Volumen beim Breakout ueber dem Durchschnitt liegen muss

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- Swing Highs/Lows via Rolling-Window erkennen
- Clustering naher Preispunkte zu Zonen
- Breakout = Close ausserhalb der Zone + Volumen-Bestaetigung
- Aufwand: **Mittel** — Zonenerkennung ist der knifflige Teil

## Varianten
- Retest-Strategie: Warten bis der Preis die Zone retestet statt sofort einzusteigen
- Fake-Breakout-Filter: Nur handeln wenn Breakout sich nach X Kerzen haelt
