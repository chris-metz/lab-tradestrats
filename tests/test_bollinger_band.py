"""Tests for the Bollinger Band scalping strategy."""

import pandas as pd
import pytest

from tradestrats.strategies.bollinger_band import BollingerBandStrategy

OHLCV_COLUMNS = ["open", "high", "low", "close", "volume"]


def _make_ohlcv(closes: list[float]) -> pd.DataFrame:
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
    """Output must contain OHLCV columns plus bb_lower, bb_mid, bb_upper, and signal."""
    data = _make_ohlcv([100.0 + i for i in range(30)])
    result = BollingerBandStrategy().generate_signals(data)

    for col in [*OHLCV_COLUMNS, "bb_lower", "bb_mid", "bb_upper", "signal"]:
        assert col in result.columns, f"Missing column: {col}"


def test_signals_values():
    """Signal column must only contain -1, 0, or 1."""
    data = _make_ohlcv([100.0 + i for i in range(30)])
    result = BollingerBandStrategy().generate_signals(data)

    assert set(result["signal"].unique()).issubset({-1, 0, 1})


def test_below_lower_band_generates_buy():
    """Sharply falling prices should push close below the lower band and trigger a buy."""
    closes = [100.0] * 20 + [100.0 - i * 5 for i in range(1, 21)]
    data = _make_ohlcv(closes)
    result = BollingerBandStrategy(bb_period=20, num_std=2.0).generate_signals(data)

    buy_signals = result.loc[result["signal"] == 1]
    assert not buy_signals.empty, "Expected at least one buy signal for falling prices"


def test_above_upper_band_generates_sell():
    """Sharply rising prices should push close above the upper band and trigger a sell."""
    closes = [100.0] * 20 + [100.0 + i * 5 for i in range(1, 21)]
    data = _make_ohlcv(closes)
    result = BollingerBandStrategy(bb_period=20, num_std=2.0).generate_signals(data)

    sell_signals = result.loc[result["signal"] == -1]
    assert not sell_signals.empty, "Expected at least one sell signal for rising prices"


def test_custom_parameters():
    """Narrower bands (1 std) should produce more signals than wider bands (3 std)."""
    # Oscillation ±5 around 100 establishes std≈3. Moderate spikes to ~108/92
    # break 1-std bands (~97-103) but stay within 3-std bands (~91-109).
    base = [100.0, 105.0, 95.0, 103.0, 97.0] * 10  # 50 bars, std ≈ 3.5
    spikes = [108.0, 92.0, 107.0, 93.0, 108.0, 92.0, 100.0, 100.0,
              107.0, 93.0, 108.0, 92.0, 107.0, 93.0, 100.0, 100.0,
              106.0, 94.0, 108.0, 92.0]
    data = _make_ohlcv(base + spikes)

    narrow = BollingerBandStrategy(bb_period=20, num_std=1.0)
    result_narrow = narrow.generate_signals(data)
    signals_narrow = (result_narrow["signal"] != 0).sum()

    wide = BollingerBandStrategy(bb_period=20, num_std=3.0)
    result_wide = wide.generate_signals(data)
    signals_wide = (result_wide["signal"] != 0).sum()

    assert signals_narrow > signals_wide, (
        "Narrower bands (1 std) should produce more signals than wider bands (3 std)"
    )
