from __future__ import annotations

import numpy as np
import pandas as pd

from tradestrats.strategies.base import Strategy


class BoxTheory(Strategy):
    """Box Theory (Previous-Day Range) mean-reversion strategy.

    Draws a "box" from the previous day's high to the previous day's low.
    Sells when price enters the top zone of the box (strong seller area),
    buys when price enters the bottom zone (strong buyer area), and avoids
    trading in the middle (noise / indecision).

    When price gaps above or below the box, it is treated as an even
    stronger sell or buy zone respectively.

    Args:
        zone_pct: Fraction of the box range that counts as top/bottom zone.
            Default 0.25 means the top 25% is the sell zone, the bottom 25%
            is the buy zone, and the middle 50% is no-trade.
    """

    name = "Box Theory"
    description = "Sell near previous-day high, buy near previous-day low, avoid the middle."
    recommended_timeframe = "5m"
    recommended_sl_stop = 0.02

    def __init__(self, zone_pct: float = 0.25):
        self.zone_pct = zone_pct

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        # Determine the calendar date for each row
        df["_date"] = df.index.date

        # Compute daily high/low from the data itself
        daily_hl = df.groupby("_date").agg(
            day_high=("high", "max"),
            day_low=("low", "min"),
        )

        # Previous day's high/low (shift by one trading day)
        daily_hl["prev_high"] = daily_hl["day_high"].shift(1)
        daily_hl["prev_low"] = daily_hl["day_low"].shift(1)

        # Map back to each row
        date_to_prev_high = daily_hl["prev_high"].to_dict()
        date_to_prev_low = daily_hl["prev_low"].to_dict()

        df["box_high"] = df["_date"].map(date_to_prev_high)
        df["box_low"] = df["_date"].map(date_to_prev_low)
        df["box_mid"] = (df["box_high"] + df["box_low"]) / 2
        df["box_range"] = df["box_high"] - df["box_low"]

        # Zone thresholds
        zone_size = df["box_range"] * self.zone_pct
        df["sell_zone"] = df["box_high"] - zone_size  # above this = sell zone
        df["buy_zone"] = df["box_low"] + zone_size    # below this = buy zone

        # Generate signals
        #  1 (buy):  close is in bottom zone or below the box
        # -1 (sell): close is in top zone or above the box
        #  0 (hold): close is in the middle
        df["signal"] = 0
        df.loc[df["close"] <= df["buy_zone"], "signal"] = 1
        df.loc[df["close"] >= df["sell_zone"], "signal"] = -1

        # First day has no previous-day data — no signal
        df.loc[df["box_high"].isna(), "signal"] = 0

        # Clean up helper columns
        df.drop(columns=["_date"], inplace=True)

        return df

    def __repr__(self) -> str:
        return f"BoxTheory(zone_pct={self.zone_pct})"
