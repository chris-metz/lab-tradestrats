# Exchange Inflow/Outflow

## Kategorie
On-Chain-basiert

## Idee
Wenn grosse Mengen Coins auf Boersen fliessen (Inflow), deutet das auf Verkaufsdruck hin — Leute schicken Coins zur Boerse um zu verkaufen. Umgekehrt: Outflow von der Boerse = Coins werden in Cold Storage gebracht = bullish (HODLing).

## Logik
- **Sell-Signal**: Netflow stark positiv (grosser Inflow auf Exchanges)
- **Buy-Signal**: Netflow stark negativ (grosser Outflow von Exchanges)
- Netflow = Inflow - Outflow
- Optional: Nur beachten wenn Netflow X Standardabweichungen vom Durchschnitt abweicht

## Parameter
- `netflow_threshold_std` — Anzahl Standardabweichungen fuer Signal (default: 2.0)
- `lookback` — Fenster fuer Durchschnitts-/Std-Berechnung (default: 30 Tage)
- `asset` — Welcher Coin (BTC, ETH)

## Datenquellen
- **Glassnode**: Umfangreichste On-Chain-Daten, aber teuer (ab ~40 USD/Monat)
- **CryptoQuant**: Aehnlich, guenstigere Einstiegs-Tier
- **IntoTheBlock**: Kostenloses Tier mit begrenzten Daten
- **Blockchain.com API**: Kostenlos fuer BTC Basics

## Umsetzung
1. Neuer Fetcher mit API-Integration (Glassnode oder CryptoQuant)
2. Historische Netflow-Daten laden und cachen
3. Merge mit OHLCV, Signal-Generierung auf Netflow-Basis
- Aufwand: **Hoch** — API-Integration + ggf. API-Key-Management + Kosten

## Einschraenkungen
- Kostenpflichtige Datenquellen (ausser sehr basale BTC-Daten)
- Nur fuer grosse Coins verfuegbar (BTC, ETH, evtl. Top 20)
- Daten oft nur taeglich verfuegbar
- Latenz: On-Chain-Daten kommen mit Verzoegerung
