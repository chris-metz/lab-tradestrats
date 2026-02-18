# Box Theory

## Kategorie
Price Action — Mean-Reversion (Intraday)

## Idee
Die Box Theory basiert auf der Tagesrange des Vortags. Die Annahme: Am Tageshoch sitzt der staerkste Verkaeufer, am Tagestief der staerkste Kaeufer. In der Mitte herrscht Noise. Entsprechend wird am oberen Rand verkauft, am unteren Rand gekauft, und in der Mitte nicht gehandelt.

Urspruenglich populaer gemacht fuer Aktien und Index-Futures (ES, YM), hier adaptiert fuer Kryptomaerkte.

## Logik
1. **Box zeichnen**: Previous Day High (oben) bis Previous Day Low (unten)
2. **Mittellinie**: Arithmetisches Mittel von High und Low
3. **Drei Zonen**:
   - **Sell-Zone** (obere 25% der Box): Close >= `box_high - zone_size` → Signal: -1
   - **Buy-Zone** (untere 25% der Box): Close <= `box_low + zone_size` → Signal: 1
   - **Dead Zone** (mittlere 50%): Kein Signal → 0
4. **Gap-Handling**: Preis ueber der Box = Sell-Zone, Preis unter der Box = Buy-Zone

## Parameter
| Parameter | Default | Beschreibung |
|-----------|---------|-------------|
| `zone_pct` | 0.25 | Anteil der Box-Range, der als Top/Bottom-Zone gilt |

## Ausgabe-Spalten
- `box_high` — Vortageshoch (obere Box-Grenze)
- `box_low` — Vortagestief (untere Box-Grenze)
- `box_mid` — Mittellinie
- `box_range` — Gesamtrange der Box
- `sell_zone` — Untere Grenze der Sell-Zone
- `buy_zone` — Obere Grenze der Buy-Zone
- `signal` — 1 (buy), -1 (sell), 0 (hold)

## Empfohlene Einstellungen
- **Timeframe**: 5m (vom Autor bevorzugt), alternativ 15m oder 1h — die Strategie ist fuer Intraday-Trading konzipiert. Die Box wird immer aus der Tagescandle des Vortags berechnet, gehandelt wird auf dem kleineren Timeframe.
- **Stop-Loss**: Knapp ausserhalb der Box-Grenze (1.5–3%), nicht der Standard von 5%
- **Take-Profit**: Mittellinie oder gegenueberliegende Box-Seite

## Geeignete Maerkte
Die Strategie wurde urspruenglich fuer **Aktien** (AAPL) und **Index-Futures** (ES, YM) entwickelt und dort demonstriert. Diese Maerkte haben klare Handelssessions mit definiertem Open/Close, was die Vortages-High/Low-Levels besonders aussagekraeftig macht.

**Krypto-Maerkte**: Eingeschraenkt geeignet. Krypto handelt 24/7 ohne Session-Grenzen, was die Bedeutung der "Tagesrange" verwischt. Zusaetzlich sind Krypto-Maerkte haeufiger in starken Trends, wo Mean-Reversion-Strategien grundsaetzlich schlechter performen. Am ehesten funktioniert die Box Theory bei Krypto in Seitwaerts-/Range-Phasen.

## Nutzung
```bash
# 5-Minuten-Candles (wie im Original-Video empfohlen)
uv run tradestrats backtest -S box -t 5m BTC/USDT

# 15-Minuten-Candles
uv run tradestrats backtest -S box -t 15m --sl 0.02 BTC/USDT

# 1-Stunden-Candles
uv run tradestrats backtest -S box -t 1h --sl 0.02 BTC/USDT
```

## Backtest-Referenz (BTC/USDT, 1h, 6 Monate, 5% SL)
- Win Rate: ~56%
- 62 Trades
- Hinweis: Negative Gesamtrendite in Trendmaerkten erwartet — Strategie ist fuer Range-Maerkte und traditionelle Maerkte (Aktien, Futures) optimiert

## Quelle
YouTube: ["If I Wanted to Make $1,000 a Day Trading, I'd Do This"](https://www.youtube.com/watch?v=r7XuZm8Ha8k) — Doug (Box Theory / Previous-Day Range)
