from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import vectorbt as vbt

from tradestrats.strategies.base import Strategy


@dataclass
class BacktestResult:
    """Container for backtest results."""

    portfolio: vbt.Portfolio
    signals: pd.DataFrame

    @property
    def total_return(self) -> float:
        return self.portfolio.total_return()

    @property
    def sharpe_ratio(self) -> float:
        return self.portfolio.sharpe_ratio()

    @property
    def max_drawdown(self) -> float:
        return self.portfolio.max_drawdown()

    @property
    def total_trades(self) -> int:
        return self.portfolio.trades.count()

    @property
    def win_rate(self) -> float:
        trades = self.portfolio.trades
        if trades.count() == 0:
            return 0.0
        return trades.win_rate()

    @property
    def equity_curve(self) -> pd.Series:
        return self.portfolio.value()

    def summary(self) -> dict:
        """Return a summary dict of key metrics."""
        return {
            "total_return": self.total_return,
            "sharpe_ratio": self.sharpe_ratio,
            "max_drawdown": self.max_drawdown,
            "total_trades": self.total_trades,
            "win_rate": self.win_rate,
        }


def run(
    strategy: Strategy,
    data: pd.DataFrame,
    init_cash: float = 10_000.0,
    fees: float = 0.001,
    sl_stop: float = 0.05,
) -> BacktestResult:
    """Run a backtest for the given strategy on OHLCV data.

    Args:
        strategy: A Strategy instance that generates signals.
        data: OHLCV DataFrame (DatetimeIndex, columns: open/high/low/close/volume).
        init_cash: Starting cash for the portfolio.
        fees: Trading fee as a fraction (e.g. 0.001 = 0.1%).
        sl_stop: Stop-loss as a fraction (e.g. 0.05 = 5%).

    Returns:
        BacktestResult with portfolio and signal data.
    """
    signals = strategy.generate_signals(data)

    # Convert signal column to entries/exits for vectorbt
    # entries: signal changes from non-1 to 1 (buy)
    # exits: signal changes from non-(-1) to -1 (sell)
    entries = (signals["signal"] == 1) & (signals["signal"].shift(1) != 1)
    exits = (signals["signal"] == -1) & (signals["signal"].shift(1) != -1)

    # Detect frequency from the DatetimeIndex; fall back to median diff
    freq = data.index.freq
    if freq is None:
        freq = pd.tseries.frequencies.to_offset(data.index.to_series().diff().median())

    portfolio = vbt.Portfolio.from_signals(
        close=data["close"],
        entries=entries,
        exits=exits,
        init_cash=init_cash,
        fees=fees,
        sl_stop=sl_stop,
        freq=freq,
    )

    return BacktestResult(portfolio=portfolio, signals=signals)
