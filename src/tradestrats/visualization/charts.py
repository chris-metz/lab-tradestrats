from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_candlestick(
    data: pd.DataFrame,
    indicators: dict[str, pd.Series] | None = None,
    title: str = "Price Chart",
) -> go.Figure:
    """Plot an interactive candlestick chart with optional indicator overlays.

    Args:
        data: OHLCV DataFrame (DatetimeIndex).
        indicators: Dict mapping indicator names to Series to overlay on chart.
        title: Chart title.

    Returns:
        Plotly Figure object.
    """
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.7, 0.3],
    )

    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["open"],
            high=data["high"],
            low=data["low"],
            close=data["close"],
            name="OHLC",
        ),
        row=1, col=1,
    )

    # Add indicator overlays
    if indicators:
        for name, series in indicators.items():
            fig.add_trace(
                go.Scatter(x=series.index, y=series, mode="lines", name=name),
                row=1, col=1,
            )

    # Volume bars
    colors = ["red" if c < o else "green" for c, o in zip(data["close"], data["open"])]
    fig.add_trace(
        go.Bar(x=data.index, y=data["volume"], name="Volume", marker_color=colors),
        row=2, col=1,
    )

    fig.update_layout(
        title=title,
        xaxis_rangeslider_visible=False,
        height=700,
        template="plotly_dark",
    )

    return fig


def plot_equity_curve(equity: pd.Series, title: str = "Equity Curve") -> go.Figure:
    """Plot the equity curve from a backtest result.

    Args:
        equity: Series with portfolio value over time.
        title: Chart title.

    Returns:
        Plotly Figure object.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=equity.index,
            y=equity,
            mode="lines",
            name="Portfolio Value",
            fill="tozeroy",
        )
    )

    fig.update_layout(
        title=title,
        yaxis_title="Value",
        xaxis_title="Date",
        height=400,
        template="plotly_dark",
    )

    return fig


def plot_signals(
    data: pd.DataFrame,
    signals: pd.DataFrame,
    title: str = "Trading Signals",
) -> go.Figure:
    """Plot price chart with buy/sell signal markers.

    Args:
        data: OHLCV DataFrame.
        signals: DataFrame with a 'signal' column (1=buy, -1=sell).
        title: Chart title.

    Returns:
        Plotly Figure object.
    """
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["close"],
            mode="lines",
            name="Close",
            line=dict(color="white", width=1),
        )
    )

    # Buy signals (where signal transitions to 1)
    buy_mask = (signals["signal"] == 1) & (signals["signal"].shift(1) != 1)
    buy_points = data.loc[buy_mask]
    fig.add_trace(
        go.Scatter(
            x=buy_points.index,
            y=buy_points["close"],
            mode="markers",
            name="Buy",
            marker=dict(symbol="triangle-up", size=12, color="lime"),
        )
    )

    # Sell signals (where signal transitions to -1)
    sell_mask = (signals["signal"] == -1) & (signals["signal"].shift(1) != -1)
    sell_points = data.loc[sell_mask]
    fig.add_trace(
        go.Scatter(
            x=sell_points.index,
            y=sell_points["close"],
            mode="markers",
            name="Sell",
            marker=dict(symbol="triangle-down", size=12, color="red"),
        )
    )

    fig.update_layout(
        title=title,
        yaxis_title="Price",
        xaxis_title="Date",
        height=500,
        template="plotly_dark",
    )

    return fig
