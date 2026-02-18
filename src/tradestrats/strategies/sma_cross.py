from __future__ import annotations

import pandas as pd
import pandas_ta as ta

from tradestrats.strategies.base import Strategy


class SMACrossover(Strategy):
    """Simple Moving Average Crossover strategy.

    Generates a buy signal when the fast SMA crosses above the slow SMA,
    and a sell signal when the fast SMA crosses below.
    """

    name = "SMA Crossover"
    description = "Buy when fast SMA crosses above slow SMA, sell on cross below."

    def __init__(self, fast_period: int = 20, slow_period: int = 50):
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        df = data.copy()

        df["sma_fast"] = ta.sma(df["close"], length=self.fast_period)
        df["sma_slow"] = ta.sma(df["close"], length=self.slow_period)

        # Signal: 1 when fast > slow, -1 when fast < slow
        df["signal"] = 0
        df.loc[df["sma_fast"] > df["sma_slow"], "signal"] = 1
        df.loc[df["sma_fast"] < df["sma_slow"], "signal"] = -1

        return df

    def __repr__(self) -> str:
        return f"SMACrossover(fast={self.fast_period}, slow={self.slow_period})"
