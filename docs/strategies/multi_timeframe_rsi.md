# Multi-Timeframe RSI

## Kategorie
Indikator-basiert — Multi-Timeframe-Konfluenz

## Idee
RSI auf mehreren Zeitrahmen gleichzeitig pruefen. Nur handeln wenn alle Timeframes das gleiche Signal geben. Reduziert Fehlsignale drastisch.

## Logik
- Berechne RSI auf z.B. 1h, 4h und 1d gleichzeitig
- **Buy**: RSI ueberverkauft auf ALLEN Timeframes (oder Mehrheit)
- **Sell**: RSI ueberkauft auf ALLEN Timeframes
- Hoeherer Timeframe hat Vorrang bei Konflikten

## Parameter
- `timeframes` — Liste der Zeitrahmen (z.B. ["1h", "4h", "1d"])
- `rsi_period` — RSI-Periode (default: 14)
- `oversold` / `overbought` — Schwellenwerte (default: 30/70)
- `confluence_mode` — "all" (alle muessen stimmen) oder "majority" (Mehrheit reicht)

## Datenquellen
OHLCV auf mehreren Timeframes — Fetcher muss mehrere Zeitrahmen laden

## Umsetzung
- Mehrfacher `fetch_ohlcv()` Aufruf mit unterschiedlichen Timeframes
- Resampling des niedrigeren Timeframes oder Merge auf gemeinsamen Index
- Aufwand: **Mittel** — Daten-Alignment zwischen Timeframes ist der Knackpunkt

## Erweiterung des Frameworks
- `generate_signals()` bekommt aktuell ein einzelnes DataFrame
- Fuer Multi-Timeframe: Entweder vorher mergen, oder Signatur erweitern
- Einfachste Loesung: Hoehere Timeframes als zusaetzliche Spalten in das DataFrame mergen
