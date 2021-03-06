#!/usr/bin/python
# -*- coding: utf-8 -*-

# performance.py

import numpy as np
import pandas
import pandas as pd

# todo 补全指标计算
from backend.commons.enums.symbol_type import SymbolTypeEnum


def create_sharpe_ratio(returns, symbol_type: SymbolTypeEnum) -> float:
    """
    Create the Sharpe ratio for the strategy, based on a
    benchmark of zero (i.e. no risk-free rate information).

    Parameters:
    returns - A pandas Series representing period percentage returns.
    periods - Daily (252), Hourly (252*6.5), Minutely(252*6.5*60) etc.
    """
    if symbol_type == SymbolTypeEnum.CHINA_STOCK:
        periods = 252
        return np.sqrt(periods) * (np.mean(returns)) / np.std(returns)


def create_draw_downs(pnl: pandas.Series) -> (pandas.Series, float, int):
    """
    Calculate the largest peak-to-trough drawdown of the PnL curve
    as well as the duration of the drawdown. Requires that the
    pnl_returns is a pandas Series.

    Parameters:
    pnl - A pandas Series representing period percentage returns.

    Returns:
    drawdown, duration - Highest peak-to-trough drawdown and duration.
    """

    # Calculate the cumulative returns curve
    # and set up the High Water Mark
    hwm = [0]

    # Create the drawdown and duration series
    idx = pnl.index
    draw_down = pd.Series(index=idx)
    duration = pd.Series(index=idx)

    # Loop over the index range
    for t in range(1, len(idx)):
        hwm.append(max(hwm[t - 1], pnl[t]))
        draw_down[t] = (hwm[t] - pnl[t])
        duration[t] = (0 if draw_down[t] == 0 else duration[t - 1] + 1)
    return draw_down, draw_down.max(), duration.max()
