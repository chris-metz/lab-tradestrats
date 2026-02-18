# Range Breakout (Squeeze)

## Kategorie
Price Action / Volatilitaet

## Idee
Maerkte wechseln zwischen Phasen niedriger Volatilitaet (Konsolidierung) und hoher Volatilitaet (Expansion). Nach einer engen Range ("Squeeze") kommt oft ein starker Ausbruch. Ziel: den Squeeze erkennen und beim Breakout einsteigen.

## Logik
- Erkenne Squeeze: Bollinger Bands innerhalb der Keltner Channels (oder ATR nahe Minimum)
- **Buy**: Squeeze endet + Preis bricht nach oben aus
- **Sell**: Squeeze endet + Preis bricht nach unten aus
- Alternativ: Nur Long-Seite handeln in Aufwaertstrend

## Parameter
- `bb_period` / `bb_std` — Bollinger Band Einstellungen
- `kc_period` / `kc_atr_mult` — Keltner Channel Einstellungen
- `squeeze_bars` — Mindestanzahl Kerzen im Squeeze
- `momentum_indicator` — Welcher Indikator die Ausbruchsrichtung bestimmt (z.B. Momentum, MACD)

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- `pandas-ta` hat `ta.squeeze()` (TTM Squeeze) — fast fertige Loesung
- Aufwand: **Gering** — squeeze-Indikator existiert bereits in pandas-ta

## Bekannt als
- TTM Squeeze (John Carter)
- Bollinger Band Squeeze
- Volatility Contraction Pattern (VCP)
