# MACD Crossover

## Kategorie
Indikator-basiert — Momentum

## Idee
Der MACD (Moving Average Convergence Divergence) zeigt das Verhaeltnis zweier EMAs zueinander. Kreuzt die MACD-Linie die Signal-Linie, deutet das auf eine Trendaenderung hin.

## Logik
- **Buy**: MACD-Linie kreuzt Signal-Linie von unten nach oben
- **Sell**: MACD-Linie kreuzt Signal-Linie von oben nach unten
- Optional: Nur handeln wenn Histogramm-Staerke einen Schwellenwert ueberschreitet
- Optional: Divergenz zwischen Preis und MACD als zusaetzliches Signal

## Parameter
- `fast_period` — Schnelle EMA (default: 12)
- `slow_period` — Langsame EMA (default: 26)
- `signal_period` — Signal-Linie EMA (default: 9)
- `histogram_threshold` — Mindest-Histogramm-Wert fuer Einstieg

## Datenquellen
OHLCV — bereits vorhanden

## Umsetzung
- `pandas-ta` hat `ta.macd()` — eine Zeile Code
- Aufwand: **Sehr gering** — fast identisch zur SMA-Crossover-Implementierung

## Varianten
- MACD + RSI Konfluenz (nur kaufen wenn MACD bullish UND RSI ueberverkauft)
- MACD Histogram Reversal (Histogramm dreht, ohne Linienkreuzung)
- Zero-Line Crossover (MACD kreuzt Nulllinie)
