# Fear & Greed Index

## Kategorie
Sentiment-basiert — Contrarian

## Idee
Der Crypto Fear & Greed Index misst die Marktstimmung auf einer Skala von 0 (Extreme Fear) bis 100 (Extreme Greed). Contrarian-Ansatz: Kaufen wenn alle Angst haben, verkaufen wenn alle gierig sind. "Be fearful when others are greedy, and greedy when others are fearful." (Buffett)

## Logik
- **Buy**: Fear & Greed Index < 20 (Extreme Fear)
- **Sell**: Fear & Greed Index > 80 (Extreme Greed)
- Optional: Nur handeln wenn der Index X Tage in der Zone bleibt (vermeidet kurze Ausschlaege)
- Optional: Mit Preis-Action kombinieren (z.B. Fear + bullisches Candlestick = staerkeres Signal)

## Parameter
- `fear_threshold` — Ab welchem Wert kaufen (default: 20)
- `greed_threshold` — Ab welchem Wert verkaufen (default: 80)
- `min_days_in_zone` — Mindestanzahl Tage in der Zone (default: 1)
- `combine_with_price` — Preis-Bestaetigung erfordern (ja/nein)

## Datenquellen
- **Alternative.me API**: `https://api.alternative.me/fng/?limit=0&format=json`
- Kostenlos, kein API-Key noetig
- Liefert taegliche Werte (historisch verfuegbar)
- Muss als neuer Fetcher implementiert werden

## Umsetzung
1. Neuer Fetcher: `data/fear_greed_fetcher.py` — holt historische F&G-Daten
2. Merge mit OHLCV-Daten auf Tages-Ebene
3. Strategie arbeitet mit `close` + `fear_greed` Spalten
- Aufwand: **Mittel** — neuer Fetcher + Merge-Logik

## Erweiterung des Frameworks
- Erster Schritt Richtung externe Datenquellen
- Fetcher-Pattern kann fuer alle weiteren Sentiment-Quellen wiederverwendet werden
- Caching analog zu OHLCV in Parquet

## Einschraenkungen
- Nur auf Tages-Ebene verfuegbar (kein Intraday)
- Primaer fuer BTC/Gesamtmarkt, nicht fuer einzelne Altcoins
- Langsamer Indikator — eher fuer Swing/Position Trading (Wochen/Monate)
