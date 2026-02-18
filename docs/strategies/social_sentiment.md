# Social Sentiment

## Kategorie
Sentiment-basiert — Social Media

## Idee
Social-Media-Aktivitaet rund um einen Coin korreliert oft mit Preisbewegungen. Explodierende Mentions koennen sowohl auf ein kommendes Pump (frueh einsteigen) als auch auf ein Top (contrarian verkaufen) hindeuten.

## Logik

### Variante 1: Momentum (mit dem Hype)
- **Buy**: Social Mentions steigen stark an (z.B. 3x Durchschnitt) + Preis steigt
- **Sell**: Mentions fallen wieder auf Normal-Niveau

### Variante 2: Contrarian (gegen den Hype)
- **Sell**: Extreme Mention-Spikes (Euphorie = Top-Signal)
- **Buy**: Social Mentions auf Tiefststand (niemand redet darueber = Boden)

## Parameter
- `mention_spike_factor` — Ab welchem Vielfachen des Durchschnitts ist es ein Spike
- `sentiment_score_threshold` — Positiv/Negativ-Schwelle des Sentiment-Scores
- `mode` — "momentum" oder "contrarian"
- `lookback` — Fenster fuer Durchschnittsberechnung

## Datenquellen
- **LunarCrush**: Social-Daten aggregiert (Twitter/X, Reddit, YouTube etc.) — kostenloser Tier verfuegbar
- **Santiment**: Social Volume, Weighted Sentiment — kostenpflichtig
- **Reddit API**: Direkt Posts/Kommentare aus r/CryptoCurrency, r/Bitcoin etc. scrapen
- **Twitter/X API**: Mentions zaehlen — eingeschraenkt seit API-Aenderungen

## Umsetzung
1. Neuer Fetcher fuer Social-Daten (LunarCrush API als einfachster Einstieg)
2. Taeglich oder stuendlich Social Volume + Sentiment Score laden
3. Merge mit OHLCV, Signal-Generierung
- Aufwand: **Mittel bis Hoch** — abhaengig von der Datenquelle

## Einschraenkungen
- Social-Daten sind verrauscht (Bots, Spam)
- API-Limits und sich aendernde Verfuegbarkeit (besonders Twitter/X)
- Zeitverzoegerung zwischen Social Spike und Preisbewegung ist variabel
- Funktioniert besser bei Small/Mid-Caps als bei BTC
