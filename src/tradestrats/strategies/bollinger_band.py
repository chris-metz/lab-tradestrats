from __future__ import annotations

import pandas as pd
import pandas_ta as ta

from tradestrats.strategies.base import Strategy


class BollingerBandStrategy(Strategy):
    """Bollinger Band scalping strategy.

    Generates a buy signal when the close price drops below the lower
    Bollinger Band (mean-reversion: expect price to bounce back toward the
    mean), and a sell signal when it rises above the upper band.
    """

    name = "Bollinger Band"
    description = "Buy when close < lower band, sell when close > upper band."

    def __init__(self, bb_period: int = 20, num_std: float = 2.0):
        self.bb_period = bb_period
        self.num_std = num_std

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        bbands = ta.bbands(
            df["close"], length=self.bb_period,
            lower_std=self.num_std, upper_std=self.num_std,
        )
        df["bb_lower"] = bbands.iloc[:, 0]
        df["bb_mid"] = bbands.iloc[:, 1]
        df["bb_upper"] = bbands.iloc[:, 2]

        df["signal"] = 0
        df.loc[df["close"] < df["bb_lower"], "signal"] = 1
        df.loc[df["close"] > df["bb_upper"], "signal"] = -1

        return df

    def __repr__(self) -> str:
        return (
            f"BollingerBandStrategy(period={self.bb_period}, "
            f"num_std={self.num_std})"
        )
