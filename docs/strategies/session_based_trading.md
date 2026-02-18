# Session-Based Trading

## Kategorie
Zeitbasiert

## Idee
Obwohl Crypto 24/7 gehandelt wird, gibt es klare Volatilitaets-Muster je nach Session (Asien, Europa, USA). Bestimmte Stunden sind profitabler als andere. Strategie: Nur in den besten Stunden/Sessions handeln.

## Bekannte Patterns
- **Asian Range Breakout**: Asiatische Session (00:00-08:00 UTC) hat oft enge Range. Europa-Open bricht diese Range.
- **US Session Momentum**: NYSE/NASDAQ Open (13:30-14:30 UTC) bringt oft starke Moves
- **Weekend Effect**: Freitag Abend bis Sonntag Abend oft niedrigere Volatilitaet
- **Month-End Rebalancing**: Letzte Tage des Monats zeigen oft bestimmte Muster

## Logik
- Definiere Trading-Windows (z.B. nur 08:00-16:00 UTC)
- Kombiniere mit einem einfachen Signal (z.B. Breakout der vorherigen Session-Range)
- **Buy**: Session-Open + Preis bricht ueber Asian Session High
- **Sell**: Session-Open + Preis bricht unter Asian Session Low
- Flat gehen vor Session-Ende

## Parameter
- `session_start` / `session_end` — Trading-Fenster (UTC)
- `reference_session_start` / `end` — Session fuer Range-Berechnung
- `breakout_buffer` — Puffer ueber/unter dem Range-High/Low (z.B. 0.1%)

## Datenquellen
OHLCV — bereits vorhanden (braucht Intraday-Daten: 1m, 5m, 15m, 1h)

## Umsetzung
- Zeitfilter auf dem Index + Range-Berechnung pro Session
- Aufwand: **Gering bis Mittel**

## Hinweis
- Funktioniert nur auf Intraday-Timeframes (nicht auf 1d)
- Session-Zeiten koennen sich saisonal verschieben (Sommer/Winterzeit)
- Backtesting sollte pro Wochentag aufgeschluesselt werden
