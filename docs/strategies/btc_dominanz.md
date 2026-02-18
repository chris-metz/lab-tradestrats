# BTC Dominanz (Kapitalrotation)

## Kategorie
Korrelations-basiert / Makro

## Idee
BTC Dominance misst den Anteil von Bitcoin an der gesamten Crypto-Marktkapitalisierung. Steigende Dominanz = Kapital fliesst von Altcoins nach BTC (Risk-Off). Fallende Dominanz = "Altseason" — Kapital fliesst in Altcoins (Risk-On).

## Logik

### Fuer BTC-Trading:
- **Buy BTC**: BTC Dominanz steigt (Kapitalfluss nach BTC)
- **Sell BTC**: BTC Dominanz faellt (Geld fliesst in Alts)

### Fuer Altcoin-Trading:
- **Buy Alts**: BTC Dominanz faellt + BTC-Preis stabil/steigend (echte Altseason)
- **Sell Alts**: BTC Dominanz steigt (Rotation zurueck zu BTC)

### Kombi-Signal:
- BTC Dominanz + BTC Preis steigt = Fruehphase Bull Market → BTC kaufen
- BTC Dominanz faellt + BTC Preis steigt = Spaetphase Bull Market → Alts kaufen
- BTC Dominanz steigt + BTC Preis faellt = Bear Market → Cash

## Parameter
- `dominance_ma_period` — Moving Average auf Dominanz (default: 14)
- `dominance_rising_threshold` — Ab wann gilt Dominanz als "steigend"
- `asset_mode` — "btc" oder "altcoin"

## Datenquellen
- **CoinGecko API**: `/global` Endpoint liefert BTC Dominanz — kostenlos
- **CoinMarketCap API**: Aehnlich — kostenloser Tier
- **TradingView**: BTC.D Chart-Daten (manuell oder via Drittanbieter)

## Umsetzung
1. Neuer Fetcher fuer BTC Dominanz (CoinGecko API)
2. Taeglich laden und mit OHLCV mergen
3. Dominanz-Trend bestimmen + Kombination mit Preistrend
- Aufwand: **Mittel** — einfache API, aber Rotations-Logik braucht Feintuning

## Einschraenkungen
- Eher Makro-Signal (Tage/Wochen, nicht Intraday)
- BTC Dominanz wird durch Stablecoins verzerrt
- Funktioniert am besten in klaren Bull/Bear Cycles
