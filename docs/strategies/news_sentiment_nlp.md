# News Sentiment (NLP)

## Kategorie
Sentiment-basiert — Natural Language Processing

## Idee
Crypto-News automatisch analysieren und das Sentiment (positiv/negativ/neutral) als Trading-Signal nutzen. Schneller als manuelles Lesen, und deckt mehr Quellen ab.

## Logik
- Sammle News-Headlines aus mehreren Quellen
- Bestimme Sentiment pro Headline (NLP-Modell oder Keyword-basiert)
- Aggregiere Sentiment-Score pro Zeiteinheit (z.B. stuendlich oder taeglich)
- **Buy**: Aggregiertes Sentiment dreht von negativ nach positiv
- **Sell**: Aggregiertes Sentiment dreht von positiv nach negativ
- Optional: Nur bei starken Ausschlaegen handeln (Threshold)

## Parameter
- `sentiment_model` — "keyword" (schnell, einfach) oder "transformer" (genauer, langsamer)
- `aggregation_period` — Zeitraum fuer Aggregation (z.B. "1h", "1d")
- `threshold_buy` / `threshold_sell` — Sentiment-Schwellenwerte
- `sources` — Welche News-Quellen einbeziehen

## Datenquellen
- **CryptoPanic API**: Aggregierte Crypto-News mit Community-Sentiment — kostenloser Tier mit API-Key
- **NewsAPI**: Allgemeine News-API — kostenloser Tier fuer Entwickler
- **RSS Feeds**: CoinDesk, CoinTelegraph, The Block etc. — kostenlos
- **Eigenes Scraping**: Flexibel, aber Wartungsaufwand

## NLP-Ansaetze
1. **Keyword-basiert**: Wortlisten (bullish/bearish Keywords) — schnell, ungenau
2. **VADER Sentiment**: Rule-based, guter Einstieg — `pip install vaderSentiment`
3. **FinBERT/CryptoBERT**: Vortrainierte Transformer-Modelle fuer Finanz-Sentiment — genau, aber braucht GPU
4. **LLM-basiert**: Claude/GPT API fuer Sentiment-Klassifikation — flexibel, aber API-Kosten

## Umsetzung
1. News-Fetcher (CryptoPanic als Einstieg)
2. Sentiment-Pipeline (VADER fuer V1, spaeter FinBERT)
3. Aggregation + Merge mit OHLCV
4. Signal-Generierung auf aggregiertem Sentiment
- Aufwand: **Hoch** — mehrere Komponenten, NLP-Pipeline

## Herausforderungen
- Latenz: News → Preisbewegung ist oft Sekunden bis Minuten
- Backtesting schwierig: Historische News mit exaktem Timestamp noetig
- Sentiment-Modelle muessen Crypto-Slang verstehen ("WAGMI", "rekt", "moon")
- Ironie/Sarkasmus ist schwer zu erkennen
