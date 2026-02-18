# ML Feature Ensemble

## Kategorie
Machine Learning

## Idee
Statt einzelne Indikatoren manuell zu kombinieren, lassen wir ein ML-Modell herausfinden welche Features relevant sind und wie sie zusammenwirken. Feature-Engineering aus allen verfuegbaren Daten, dann Klassifikation (Buy/Sell/Hold) oder Regression (erwartete Rendite).

## Ansaetze

### Einfach (guter Einstieg):
- **Random Forest / XGBoost**: Features aus technischen Indikatoren → Klassifikation
- Interpretierbar (Feature Importance), schnell zu trainieren
- Braucht keine GPU

### Mittel:
- **LSTM / GRU**: Zeitreihen-Modelle die temporale Abhaengigkeiten lernen
- Besser bei sequentiellen Mustern
- Braucht mehr Daten und Rechenleistung

### Fortgeschritten:
- **Transformer-basiert**: Attention-Mechanismus auf Zeitreihen
- **Reinforcement Learning**: Agent lernt Trading-Strategie direkt
- Sehr datenintensiv, Overfitting-Gefahr

## Moegliche Features
- Alle technischen Indikatoren (RSI, MACD, BB, ADX, OBV, ...)
- Lag-Features (Return der letzten N Kerzen)
- Volatilitaet (ATR, Bollinger Width)
- Volumen-Features (Volume Ratio, OBV Trend)
- Zeitfeatures (Stunde, Wochentag, Monat)
- Optional: Sentiment, On-Chain, Korrelationen

## Label-Generierung
- **Einfach**: Naechste Kerze gruen/rot → Binary Classification
- **Besser**: Return der naechsten N Kerzen > Threshold → Buy, < -Threshold → Sell, sonst Hold
- **Triple Barrier Method** (Lopez de Prado): Drei Schranken (Profit Target, Stop Loss, Max Holding Period) — robustestes Labeling

## Parameter
- `model_type` — "xgboost", "random_forest", "lstm"
- `feature_set` — Welche Features einbeziehen
- `label_method` — "simple", "threshold", "triple_barrier"
- `train_window` — Trainings-Fenster (z.B. 365 Tage)
- `retrain_interval` — Wie oft neu trainieren (z.B. alle 30 Tage)

## Umsetzung
1. Feature-Engineering-Pipeline (alle Indikatoren berechnen + normalisieren)
2. Label-Generierung
3. Walk-Forward Training/Testing (kein Lookahead-Bias!)
4. Signal-Generierung aus Modell-Vorhersagen
- Aufwand: **Sehr hoch** — eigenes Subprojekt

## Kritische Fallstricke
- **Overfitting**: ML-Modelle lernen Noise statt Signal → Walk-Forward Validation
- **Lookahead Bias**: Versehentlich zukuenftige Daten im Training nutzen
- **Survivorship Bias**: Nur existierende Coins backtesten
- **Regime Changes**: Modell trainiert auf Bull Market, deployed in Bear Market
- **Feature Leakage**: Features die indirekt die Zukunft enthalten

## Dependencies
- `scikit-learn` — Random Forest, Feature Engineering
- `xgboost` — Gradient Boosting
- `torch` / `tensorflow` — Fuer LSTM/Transformer (optional)

## Empfehlung
Mit XGBoost + technischen Indikatoren starten. Einfach, interpretierbar, und oft ueberraschend gut. Walk-Forward Validation ist PFLICHT.
