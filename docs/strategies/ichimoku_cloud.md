# Ichimoku Cloud

## Kategorie
Indikator-basiert — Trend-Following (Multi-Indikator-System)

## Idee
Ichimoku Kinko Hyo ist ein komplettes Handelssystem aus Japan. Es liefert auf einen Blick Trend, Momentum, Support/Resistance und Signale — alles in einem Indikator.

## Komponenten
- **Tenkan-sen** (Conversion Line): Mittelpunkt von 9-Perioden High/Low
- **Kijun-sen** (Base Line): Mittelpunkt von 26-Perioden High/Low
- **Senkou Span A** (Leading Span A): Mittelwert von Tenkan + Kijun, 26 Perioden voraus geplottet
- **Senkou Span B** (Leading Span B): Mittelpunkt von 52-Perioden High/Low, 26 Perioden voraus
- **Kumo** (Cloud): Bereich zwischen Senkou Span A und B

## Logik
- **Buy**: Preis ueber der Cloud + Tenkan kreuzt Kijun von unten (TK Cross)
- **Sell**: Preis unter der Cloud + Tenkan kreuzt Kijun von oben
- Cloud-Farbe als Trendfilter: Gruene Cloud = bullish, rote Cloud = bearish
- Staerkstes Signal: Alle 5 Bedingungen gleichzeitig erfuellt

## Parameter
- `tenkan_period` — Conversion Line (default: 9)
- `kijun_period` — Base Line (default: 26)
- `senkou_b_period` — Leading Span B (default: 52)
- `mode` — "tk_cross" (nur Crossover), "kumo_breakout" (Cloud-Ausbruch), "full" (alle Signale)

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- `pandas-ta` hat `ta.ichimoku()` — liefert alle Komponenten
- Aufwand: **Gering bis Mittel** — Indikator existiert, aber die Signallogik hat mehrere Varianten

## Hinweis
- Original fuer Wochen-Charts entwickelt (japanische Handelswochen: 9 Tage, 26 Tage, 52 Wochen)
- Bei Crypto oft angepasste Perioden (z.B. 10/30/60 fuer 24/7-Maerkte)
- Sehr gut auf hoeheren Timeframes (4h, 1d), weniger auf 1m/5m
