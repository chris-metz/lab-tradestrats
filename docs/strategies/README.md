# Strategie-Ideen

Sammlung von Strategien, die wir in Zukunft implementieren koennen. Pro Strategie ein Dokument mit Beschreibung, Logik, Datenquellen und Aufwand.

## Bereits implementiert

| Strategie | Typ | Datei |
|-----------|-----|-------|
| [SMA Crossover](../../src/tradestrats/strategies/sma_cross.py) | Trend-Following | `sma_cross.py` |
| [RSI Mean Reversion](../../src/tradestrats/strategies/rsi_mean_reversion.py) | Mean-Reversion | `rsi_mean_reversion.py` |
| [Bollinger Band Scalping](../../src/tradestrats/strategies/bollinger_band.py) | Scalping | `bollinger_band.py` |

## Ideen — nach Kategorie

### Price Action (OHLCV reicht, sofort umsetzbar)

- [Candlestick Patterns](candlestick_patterns.md) — Doji, Engulfing, Hammer etc.
- [Support/Resistance Breakout](support_resistance_breakout.md) — Ausbruch aus Preiszonen
- [Range Breakout (Squeeze)](range_breakout_squeeze.md) — Breakout nach enger Konsolidierung
- [Higher Highs / Lower Lows](higher_highs_lower_lows.md) — Strukturbasiertes Trend-Trading

### Indikator-basiert (OHLCV reicht, sofort umsetzbar)

- [MACD Crossover](macd_crossover.md) — Klassischer Momentum-Indikator
- [Stochastic RSI](stochastic_rsi.md) — Kombination aus Stochastic und RSI
- [Ichimoku Cloud](ichimoku_cloud.md) — Japanisches Multi-Indikator-System
- [VWAP Reversion](vwap_reversion.md) — Intraday Mean-Reversion zum VWAP
- [EMA Ribbon](ema_ribbon.md) — Mehrere EMAs als Trendfilter
- [ADX Trend Strength](adx_trend_strength.md) — Nur traden wenn starker Trend vorliegt
- [Multi-Timeframe RSI](multi_timeframe_rsi.md) — RSI-Konfluenz ueber mehrere Zeitrahmen

### Volumen-basiert (OHLCV reicht)

- [Volume Spike Breakout](volume_spike_breakout.md) — Ungewoehnliches Volumen als Trigger
- [OBV Divergenz](obv_divergenz.md) — On-Balance Volume Divergenz zum Preis

### Zeitbasiert (OHLCV reicht)

- [Session-Based Trading](session_based_trading.md) — Handel zu bestimmten Uhrzeiten

### Sentiment & On-Chain (externe Datenquellen noetig)

- [Fear & Greed Index](fear_and_greed.md) — Contrarian-Strategie auf Marktsentiment
- [Funding Rate Arbitrage](funding_rate.md) — Perpetual Futures Funding als Signal
- [Exchange Inflow/Outflow](exchange_inflow_outflow.md) — On-Chain Wallet-Bewegungen
- [Social Sentiment](social_sentiment.md) — Social Media Mentions als Indikator
- [News Sentiment (NLP)](news_sentiment_nlp.md) — Automatische News-Analyse
- [BTC Dominanz](btc_dominanz.md) — Kapitalrotation zwischen BTC und Alts
- [Korrelations-Trading](korrelations_trading.md) — Crypto vs. TradFi Korrelationen

### Machine Learning (erweitertes Framework noetig)

- [ML Feature Ensemble](ml_feature_ensemble.md) — Klassifikation aus kombinierten Features
