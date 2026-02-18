from __future__ import annotations

from datetime import date, timedelta

import ccxt
import pandas as pd
import streamlit as st

from tradestrats.backtesting import engine
from tradestrats.config import DEFAULT_EXCHANGE, DEFAULT_SYMBOL, TIMEFRAMES
from tradestrats.data.fetcher import fetch_ohlcv, is_stock_symbol
from tradestrats.strategies.base import Strategy
from tradestrats.strategies.bollinger_band import BollingerBandStrategy
from tradestrats.strategies.box_theory import BoxTheory
from tradestrats.strategies.rsi_mean_reversion import RSIMeanReversion
from tradestrats.strategies.sma_cross import SMACrossover
from tradestrats.visualization.charts import plot_candlestick, plot_equity_curve, plot_signals

STRATEGY_KEYS = {
    "RSI Mean Reversion": "rsi",
    "SMA Crossover": "sma",
    "Bollinger Band": "bb",
    "Box Theory": "box",
}

# Map keys to strategy classes for reading recommended defaults
_STRATEGY_CLASSES: dict[str, type[Strategy]] = {
    "rsi": RSIMeanReversion,
    "sma": SMACrossover,
    "bb": BollingerBandStrategy,
    "box": BoxTheory,
}


@st.cache_data(ttl=3600)
def _load_symbols(exchange_id: str) -> list[str]:
    """Load USDT trading pairs from the given exchange (cached for 1 hour)."""
    exchange = getattr(ccxt, exchange_id)()
    exchange.load_markets()
    symbols = sorted(s for s in exchange.symbols if s.endswith("/USDT"))
    return symbols


def _render_sidebar() -> dict:
    """Render sidebar controls and return parameter dict."""
    st.sidebar.header("Strategy")
    strategy_name = st.sidebar.selectbox("Strategy", list(STRATEGY_KEYS))
    strategy_key = STRATEGY_KEYS[strategy_name]

    params: dict = {"strategy_key": strategy_key}

    if strategy_key == "rsi":
        params["rsi_period"] = st.sidebar.number_input("RSI Period", 2, 100, 14)
        params["oversold"] = st.sidebar.number_input("Oversold", 1, 49, 30)
        params["overbought"] = st.sidebar.number_input("Overbought", 51, 99, 70)
    elif strategy_key == "sma":
        params["fast_period"] = st.sidebar.number_input("Fast Period", 2, 200, 20)
        params["slow_period"] = st.sidebar.number_input("Slow Period", 5, 500, 50)
    elif strategy_key == "bb":
        params["bb_period"] = st.sidebar.number_input("BB Period", 2, 100, 20)
        params["num_std"] = st.sidebar.number_input("Std Dev", 0.5, 5.0, 2.0, step=0.1)
    elif strategy_key == "box":
        params["zone_pct"] = st.sidebar.number_input("Zone %", 0.05, 0.50, 0.25, step=0.05, format="%.2f")

    # Read recommended defaults from the selected strategy class
    strat_cls = _STRATEGY_CLASSES[strategy_key]
    rec_tf = strat_cls.recommended_timeframe
    rec_sl = strat_cls.recommended_sl_stop

    st.sidebar.header("Market")
    market_type = st.sidebar.radio("Market", ["Crypto", "Stocks"], horizontal=True)
    params["market_type"] = market_type

    if market_type == "Crypto":
        params["exchange"] = st.sidebar.text_input("Exchange", DEFAULT_EXCHANGE)
        try:
            symbols = _load_symbols(params["exchange"])
            default_idx = symbols.index(DEFAULT_SYMBOL) if DEFAULT_SYMBOL in symbols else 0
            params["symbol"] = st.sidebar.selectbox("Symbol", symbols, index=default_idx)
        except Exception:
            params["symbol"] = st.sidebar.text_input("Symbol", DEFAULT_SYMBOL)
            symbols = []
        st.session_state["_symbols"] = symbols
    else:
        params["exchange"] = DEFAULT_EXCHANGE  # ignored for stocks
        params["symbol"] = st.sidebar.text_input("Ticker", "AAPL", help="z.B. AAPL, MSFT, ^GSPC")
        st.session_state["_symbols"] = []
    tf_index = TIMEFRAMES.index(rec_tf) if rec_tf in TIMEFRAMES else TIMEFRAMES.index("1h")
    params["timeframe"] = st.sidebar.selectbox("Timeframe", TIMEFRAMES, index=tf_index)
    default_start = date.today() - timedelta(days=180)
    params["start"] = st.sidebar.date_input("Start", default_start)
    params["end"] = st.sidebar.date_input("End", date.today())

    st.sidebar.header("Portfolio")
    params["cash"] = st.sidebar.number_input("Initial Cash", 100.0, 1_000_000.0, 10_000.0, step=1000.0)
    params["fees"] = st.sidebar.number_input("Fees", 0.0, 0.1, 0.001, step=0.0001, format="%.4f")
    params["stop_loss"] = st.sidebar.number_input("Stop-Loss", 0.0, 1.0, rec_sl, step=0.01, format="%.2f")

    params["run"] = st.sidebar.button("Run Backtest", type="primary", use_container_width=True)
    return params


def _build_strategy(params: dict) -> Strategy:
    """Instantiate a strategy from UI parameters."""
    key = params["strategy_key"]
    if key == "rsi":
        return RSIMeanReversion(
            rsi_period=params["rsi_period"],
            oversold=params["oversold"],
            overbought=params["overbought"],
        )
    if key == "sma":
        return SMACrossover(
            fast_period=params["fast_period"],
            slow_period=params["slow_period"],
        )
    if key == "box":
        return BoxTheory(zone_pct=params["zone_pct"])
    return BollingerBandStrategy(
        bb_period=params["bb_period"],
        num_std=params["num_std"],
    )


def _get_indicators(strategy_key: str, signals) -> dict | None:
    """Return indicator columns for candlestick overlay."""
    if strategy_key == "sma":
        return {"SMA Fast": signals["sma_fast"], "SMA Slow": signals["sma_slow"]}
    if strategy_key == "bb":
        return {
            "BB Lower": signals["bb_lower"],
            "BB Mid": signals["bb_mid"],
            "BB Upper": signals["bb_upper"],
        }
    if strategy_key == "box":
        return {
            "Box High": signals["box_high"],
            "Box Mid": signals["box_mid"],
            "Box Low": signals["box_low"],
        }
    return None


def _display_results(result, params: dict) -> None:
    """Render metrics and charts for a completed backtest."""
    s = result.summary()

    # Metrics — 2 rows x 3 columns
    row1 = st.columns(3)
    row1[0].metric("Total Return", f"{s['total_return']:+.2%}")
    row1[1].metric("Final Value", f"{s['final_value']:,.2f}")
    row1[2].metric("Sharpe Ratio", f"{s['sharpe_ratio']:.2f}")

    row2 = st.columns(3)
    row2[0].metric("Max Drawdown", f"{s['max_drawdown']:.2%}")
    row2[1].metric("Total Trades", f"{s['total_trades']}")
    row2[2].metric("Win Rate", f"{s['win_rate']:.2%}")

    # Charts in tabs — Markets tab only for Crypto
    show_markets = params.get("market_type", "Crypto") == "Crypto"
    tab_names = ["Price & Indicators", "Signals", "Equity Curve"]
    if show_markets:
        tab_names.append("Markets")
    tabs = st.tabs(tab_names)

    signals = result.signals
    data = signals[["open", "high", "low", "close", "volume"]]

    with tabs[0]:
        indicators = _get_indicators(params["strategy_key"], signals)
        fig = plot_candlestick(data, indicators=indicators, title=f"{params['symbol']} — Price & Indicators")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        fig = plot_signals(data, signals, title=f"{params['symbol']} — Trading Signals")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        fig = plot_equity_curve(result.equity_curve, title="Equity Curve")
        st.plotly_chart(fig, use_container_width=True)

    if show_markets:
        with tabs[3]:
            _render_markets_tab()


def _render_markets_tab() -> None:
    """Render the Markets tab with a searchable table of USDT pairs."""
    symbols = st.session_state.get("_symbols", [])
    if not symbols:
        st.info("No market data available. Check the exchange setting.")
        return
    search = st.text_input("Search symbols", key="markets_search")
    rows = []
    for s in symbols:
        base, quote = s.split("/")
        rows.append({"Symbol": s, "Base": base, "Quote": quote})
    df = pd.DataFrame(rows)
    if search:
        df = df[df["Symbol"].str.contains(search.upper(), case=False)]
    st.dataframe(df, use_container_width=True, hide_index=True)


def main() -> None:
    st.set_page_config(page_title="tradestrats", page_icon=":chart_with_upwards_trend:", layout="wide")
    st.title("tradestrats — Backtesting Dashboard")

    params = _render_sidebar()

    if params["run"]:
        try:
            with st.spinner("Fetching data & running backtest..."):
                data = fetch_ohlcv(
                    symbol=params["symbol"],
                    timeframe=params["timeframe"],
                    start=str(params["start"]),
                    end=str(params["end"]),
                    exchange_id=params["exchange"],
                )
                strategy = _build_strategy(params)
                result = engine.run(
                    strategy, data,
                    init_cash=params["cash"],
                    fees=params["fees"],
                    sl_stop=params["stop_loss"],
                )
            st.session_state["result"] = result
            st.session_state["params"] = params
        except Exception as exc:
            st.error(f"Backtest failed: {exc}")

    if "result" in st.session_state:
        _display_results(st.session_state["result"], st.session_state["params"])
    elif params.get("market_type", "Crypto") == "Crypto":
        tab_markets, = st.tabs(["Markets"])
        with tab_markets:
            _render_markets_tab()


if __name__ == "__main__":
    main()
