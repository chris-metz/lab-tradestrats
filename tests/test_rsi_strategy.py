"""Tests for the RSI Mean-Reversion strategy."""

import numpy as np
import pandas as pd
import pytest

from tradestrats.strategies.rsi_mean_reversion import RSIMeanReversion

OHLCV_COLUMNS = ["open", "high", "low", "close", "volume"]


def _make_ohlcv(closes: list[float], length: int | None = None) -> pd.DataFrame:
    """Build a minimal OHLCV DataFrame from a list of close prices."""
    n = len(closes)
    return pd.DataFrame(
        {
            "open": closes,
            "high": [c * 1.01 for c in closes],
            "low": [c * 0.99 for c in closes],
            "close": closes,
            "volume": [100.0] * n,
        },
        index=pd.date_range("2024-01-01", periods=n, freq="1D"),
    )


def test_generate_signals_columns():
    """Output must contain OHLCV columns plus rsi and signal."""
    data = _make_ohlcv([100.0 + i for i in range(30)])
    result = RSIMeanReversion().generate_signals(data)

    for col in [*OHLCV_COLUMNS, "rsi", "signal"]:
        assert col in result.columns, f"Missing column: {col}"


def test_signals_values():
    """Signal column must only contain -1, 0, or 1."""
    data = _make_ohlcv([100.0 + i for i in range(30)])
    result = RSIMeanReversion().generate_signals(data)

    assert set(result["signal"].unique()).issubset({-1, 0, 1})


def test_oversold_generates_buy():
    """Steadily falling prices should push RSI below 30 and trigger a buy."""
    # Steep decline over 20 bars drives RSI well below 30
    closes = [100.0 - i * 3 for i in range(20)]
    data = _make_ohlcv(closes)
    result = RSIMeanReversion(rsi_period=14).generate_signals(data)

    buy_signals = result.loc[result["signal"] == 1]
    assert not buy_signals.empty, "Expected at least one buy signal for falling prices"


def test_overbought_generates_sell():
    """Steadily rising prices should push RSI above 70 and trigger a sell."""
    closes = [100.0 + i * 3 for i in range(20)]
    data = _make_ohlcv(closes)
    result = RSIMeanReversion(rsi_period=14).generate_signals(data)

    sell_signals = result.loc[result["signal"] == -1]
    assert not sell_signals.empty, "Expected at least one sell signal for rising prices"


def test_custom_parameters():
    """Custom oversold/overbought thresholds should be respected."""
    # V-shape: drop then recover → RSI goes low then climbs back through a range
    closes = [100.0 - i * 2 for i in range(20)] + [62.0 + i * 2 for i in range(20)]
    data = _make_ohlcv(closes)

    # Default oversold=30 should catch the low-RSI bars
    default = RSIMeanReversion(rsi_period=14, oversold=30, overbought=70)
    result_default = default.generate_signals(data)
    buys_default = (result_default["signal"] == 1).sum()

    # Lowering oversold to 10 should catch fewer bars (only the very lowest RSI)
    strict = RSIMeanReversion(rsi_period=14, oversold=10, overbought=70)
    result_strict = strict.generate_signals(data)
    buys_strict = (result_strict["signal"] == 1).sum()

    assert buys_default > buys_strict, (
        "Wider oversold threshold should produce more buy signals than stricter one"
    )
