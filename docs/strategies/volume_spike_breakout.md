# Volume Spike Breakout

## Kategorie
Volumen-basiert

## Idee
Ungewoehnlich hohes Volumen deutet auf institutionelle Aktivitaet oder wichtige Marktereignisse hin. Ein Preisausbruch mit Volumen-Spike hat eine hoehere Wahrscheinlichkeit, sich fortzusetzen, als ein Ausbruch mit normalem Volumen.

## Logik
- Berechne durchschnittliches Volumen (z.B. SMA 20)
- Erkenne Volumen-Spike: Aktuelles Volumen > X * Durchschnitt
- **Buy**: Volumen-Spike + gruene Kerze (Close > Open) + Close ueber vorherigem High
- **Sell**: Volumen-Spike + rote Kerze (Close < Open) + Close unter vorherigem Low
- Optional: Bestaetigung in der naechsten Kerze abwarten

## Parameter
- `volume_ma_period` — Fenster fuer Durchschnittsvolumen (default: 20)
- `spike_factor` — Ab welchem Vielfachen des Durchschnitts ist es ein Spike (default: 2.0)
- `require_breakout` — Muss der Preis auch ein neues High/Low machen (ja/nein)

## Datenquellen
OHLCV — bereits vorhanden (Volume-Spalte)

## Umsetzung
- Volumen-SMA + Spike-Erkennung + Richtungsfilter
- Aufwand: **Gering**

## Kombinationen
- Sehr gut als Bestaetigung fuer andere Strategien (Support/Resistance Breakout, Range Breakout)
- Volume Spike ohne Preis-Breakout = moegliche Akkumulation/Distribution (fruehes Signal)
