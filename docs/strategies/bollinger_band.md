# Bollinger Band Scalping

## Kategorie
Indikator-basiert — Scalping / Mean-Reversion

## Idee
Bollinger Baender bestehen aus einem gleitenden Durchschnitt (Mitte) und zwei Standardabweichungs-Baendern. Wenn der Preis das untere Band durchbricht, gilt er als ueberverkauft und eine Rueckkehr zur Mitte wird erwartet. Umgekehrt beim oberen Band.

## Logik
- **Buy**: `close < bb_lower` (Preis unter dem unteren Bollinger Band)
- **Sell**: `close > bb_upper` (Preis ueber dem oberen Bollinger Band)
- **Hold**: Preis liegt innerhalb der Baender

## Parameter
| Parameter | Default | Beschreibung |
|-----------|---------|-------------|
| `bb_period` | 20 | Periode des gleitenden Durchschnitts |
| `num_std` | 2.0 | Anzahl Standardabweichungen fuer die Baender |

## Ausgabe-Spalten
- `bb_lower` — Unteres Bollinger Band
- `bb_mid` — Mittleres Band (SMA)
- `bb_upper` — Oberes Bollinger Band
- `signal` — 1 (buy), -1 (sell), 0 (hold)

## Empfohlene Einstellungen (Defaults)
| Einstellung | Wert | Begruendung |
|-------------|------|-------------|
| Timeframe | `1h` | Scalping auf Stundenbasis, genug Daten fuer BB-Berechnung |
| Stop-Loss | 3% | Engerer Stop als Trend-Strategien, da Mean-Reversion kleinere Swings handelt |

Diese Werte werden automatisch verwendet wenn `-t` bzw. `--sl` nicht angegeben werden.

## Nutzung
```bash
# Mit empfohlenen Defaults (1h, 3% SL)
uv run tradestrats backtest -S bb BTC/USDT

# Manuell ueberschreiben
uv run tradestrats backtest -S bb -t 15m --sl 0.02 BTC/USDT
```

## Staerken & Schwaechen
- **Staerke**: Passt sich automatisch an Volatilitaet an, guter Scalping-Ansatz
- **Schwaeche**: In starken Trends kann der Preis lange ausserhalb der Baender bleiben
