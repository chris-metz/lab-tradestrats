"""Tests for the Box Theory strategy."""

import numpy as np
import pandas as pd
import pytest

from tradestrats.strategies.box_theory import BoxTheory


def _make_multi_day_ohlcv(
    day1_closes: list[float],
    day2_closes: list[float],
    day1_high: float | None = None,
    day1_low: float | None = None,
) -> pd.DataFrame:
    """Build OHLCV data spanning two days with hourly candles.

    Day 1 establishes the box; Day 2 is where signals are generated.
    """
    n1, n2 = len(day1_closes), len(day2_closes)
    closes = day1_closes + day2_closes

    # Default high/low from closes if not explicitly given
    highs, lows = [], []
    for i, c in enumerate(closes):
        if i < n1:
            h = max(c * 1.005, day1_high) if day1_high else c * 1.005
            lo = min(c * 0.995, day1_low) if day1_low else c * 0.995
        else:
            h = c * 1.002
            lo = c * 0.998
        highs.append(h)
        lows.append(lo)

    # Force day 1's actual high/low to match specified values
    if day1_high is not None:
        peak_idx = np.argmax(day1_closes)
        highs[peak_idx] = day1_high
    if day1_low is not None:
        trough_idx = np.argmin(day1_closes)
        lows[trough_idx] = day1_low

    index = pd.date_range("2024-01-01", periods=n1, freq="1h").append(
        pd.date_range("2024-01-02", periods=n2, freq="1h")
    )
    return pd.DataFrame(
        {
            "open": closes,
            "high": highs,
            "low": lows,
            "close": closes,
            "volume": [1000.0] * (n1 + n2),
        },
        index=index,
    )


def test_output_columns():
    """Output must contain box levels and signal column."""
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0] * 8,
        day2_closes=[100.0] * 8,
    )
    result = BoxTheory().generate_signals(data)

    for col in ["box_high", "box_low", "box_mid", "signal"]:
        assert col in result.columns, f"Missing column: {col}"


def test_signal_values():
    """Signal column must only contain -1, 0, or 1."""
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0] * 8,
        day2_closes=[100.0] * 8,
    )
    result = BoxTheory().generate_signals(data)
    assert set(result["signal"].unique()).issubset({-1, 0, 1})


def test_buy_signal_at_bottom():
    """Price near the bottom of the box should generate a buy signal."""
    # Day 1: range 90-110 → box_high=110, box_low=90
    # Day 2: price sits at 92 (near bottom)
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0, 110.0, 95.0, 90.0, 100.0, 105.0, 98.0, 100.0],
        day2_closes=[92.0, 91.0, 90.5, 91.5, 92.0, 91.0, 90.0, 91.0],
        day1_high=110.0,
        day1_low=90.0,
    )
    result = BoxTheory(zone_pct=0.25).generate_signals(data)

    day2_signals = result.loc["2024-01-02"]
    buy_count = (day2_signals["signal"] == 1).sum()
    assert buy_count > 0, "Expected buy signals when price is near box bottom"


def test_sell_signal_at_top():
    """Price near the top of the box should generate a sell signal."""
    # Day 1: range 90-110 → box_high=110, box_low=90
    # Day 2: price sits at 108 (near top)
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0, 110.0, 95.0, 90.0, 100.0, 105.0, 98.0, 100.0],
        day2_closes=[108.0, 109.0, 109.5, 108.5, 109.0, 108.0, 110.0, 109.0],
        day1_high=110.0,
        day1_low=90.0,
    )
    result = BoxTheory(zone_pct=0.25).generate_signals(data)

    day2_signals = result.loc["2024-01-02"]
    sell_count = (day2_signals["signal"] == -1).sum()
    assert sell_count > 0, "Expected sell signals when price is near box top"


def test_hold_in_middle():
    """Price in the middle of the box should generate hold (0) signals."""
    # Day 1: range 90-110 → box mid = 100
    # Day 2: price sits right at 100 (dead center)
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0, 110.0, 95.0, 90.0, 100.0, 105.0, 98.0, 100.0],
        day2_closes=[100.0, 100.5, 99.5, 100.0, 100.5, 99.5, 100.0, 100.0],
        day1_high=110.0,
        day1_low=90.0,
    )
    result = BoxTheory(zone_pct=0.25).generate_signals(data)

    day2_signals = result.loc["2024-01-02"]
    assert (day2_signals["signal"] == 0).all(), "Expected hold signals in the middle of the box"


def test_no_signal_on_first_day():
    """First day has no previous-day data, so all signals should be 0."""
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0] * 8,
        day2_closes=[100.0] * 8,
    )
    result = BoxTheory().generate_signals(data)

    day1_signals = result.loc["2024-01-01"]
    assert (day1_signals["signal"] == 0).all(), "First day should have no signals"


def test_gap_above_box_is_sell():
    """Price gapping far above the box should be treated as sell zone."""
    # Day 1: range 90-110
    # Day 2: price gaps up to 120 (well above box high of 110)
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0, 110.0, 95.0, 90.0, 100.0, 105.0, 98.0, 100.0],
        day2_closes=[120.0, 121.0, 119.0, 120.0, 122.0, 121.0, 120.0, 119.0],
        day1_high=110.0,
        day1_low=90.0,
    )
    result = BoxTheory(zone_pct=0.25).generate_signals(data)

    day2_signals = result.loc["2024-01-02"]
    assert (day2_signals["signal"] == -1).all(), "Gap above box should all be sell signals"


def test_gap_below_box_is_buy():
    """Price gapping far below the box should be treated as buy zone."""
    # Day 1: range 90-110
    # Day 2: price gaps down to 80 (well below box low of 90)
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0, 110.0, 95.0, 90.0, 100.0, 105.0, 98.0, 100.0],
        day2_closes=[80.0, 79.0, 81.0, 80.0, 78.0, 79.0, 80.0, 81.0],
        day1_high=110.0,
        day1_low=90.0,
    )
    result = BoxTheory(zone_pct=0.25).generate_signals(data)

    day2_signals = result.loc["2024-01-02"]
    assert (day2_signals["signal"] == 1).all(), "Gap below box should all be buy signals"


def test_custom_zone_pct():
    """Wider zone_pct should generate more signals than narrower one."""
    data = _make_multi_day_ohlcv(
        day1_closes=[100.0, 110.0, 95.0, 90.0, 100.0, 105.0, 98.0, 100.0],
        day2_closes=[92.0, 95.0, 100.0, 105.0, 108.0, 103.0, 97.0, 92.0],
        day1_high=110.0,
        day1_low=90.0,
    )

    wide = BoxTheory(zone_pct=0.40).generate_signals(data)
    narrow = BoxTheory(zone_pct=0.10).generate_signals(data)

    wide_trades = (wide.loc["2024-01-02", "signal"] != 0).sum()
    narrow_trades = (narrow.loc["2024-01-02", "signal"] != 0).sum()

    assert wide_trades >= narrow_trades, "Wider zone should produce at least as many signals"
