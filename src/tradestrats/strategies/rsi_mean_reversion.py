from __future__ import annotations

import pandas as pd
import pandas_ta as ta

from tradestrats.strategies.base import Strategy


class RSIMeanReversion(Strategy):
    """RSI Mean-Reversion strategy.

    Generates a buy signal when RSI drops below the oversold threshold
    (mean-reversion: expect price to bounce back up), and a sell signal
    when RSI rises above the overbought threshold.
    """

    name = "RSI Mean Reversion"
    description = "Buy when RSI < oversold, sell when RSI > overbought."
    recommended_timeframe = "1h"
    recommended_sl_stop = 0.05

    def __init__(
        self,
        rsi_period: int = 14,
        oversold: float = 30,
        overbought: float = 70,
    ):
        self.rsi_period = rsi_period
        self.oversold = oversold
        self.overbought = overbought

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        df["rsi"] = ta.rsi(df["close"], length=self.rsi_period)

        df["signal"] = 0
        df.loc[df["rsi"] < self.oversold, "signal"] = 1
        df.loc[df["rsi"] > self.overbought, "signal"] = -1

        return df

    def __repr__(self) -> str:
        return (
            f"RSIMeanReversion(period={self.rsi_period}, "
            f"oversold={self.oversold}, overbought={self.overbought})"
        )
