from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd


class Strategy(ABC):
    """Abstract base class for trading strategies.

    Subclasses must implement `generate_signals` which takes OHLCV data
    and returns a DataFrame with at least a 'signal' column containing
    1 (buy), -1 (sell), or 0 (hold).
    """

    name: str = "BaseStrategy"
    description: str = ""
    recommended_timeframe: str = "1h"
    recommended_sl_stop: float = 0.05

    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate trading signals from OHLCV data.

        Args:
            data: DataFrame with columns open, high, low, close, volume.

        Returns:
            DataFrame with a 'signal' column (1=buy, -1=sell, 0=hold)
            and any additional indicator columns used by the strategy.
        """

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r})"
