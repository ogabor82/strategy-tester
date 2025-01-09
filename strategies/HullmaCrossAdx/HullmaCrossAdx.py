import pandas as pd
import ta
import numpy as np

from backtesting import Strategy
from backtesting.lib import crossover


def HullMovingAverage(closes: pd.Series, n: int) -> pd.Series:
    def wma(series, period):
        weights = np.arange(1, period + 1)
        wma = np.zeros_like(series)
        for i in range(period - 1, len(series)):
            wma[i] = np.sum(series[i - period + 1 : i + 1] * weights) / np.sum(weights)
        return wma

    # Calculate the weighted moving averages
    wma_n = wma(closes, n)
    wma_n2 = wma(closes, n // 2)

    # Calculate the raw HMA
    raw_hma = 2 * wma_n2 - wma_n

    # Calculate the final HMA
    sqrt_n = int(pow(n, 0.5))
    hma = wma(raw_hma, sqrt_n)

    return hma


class HullmaCrossAdx(Strategy):
    hma_fast = 20
    hma_slow = 40
    adx = 14
    adx_threshold = 10

    def init(self):
        self.hma1 = self.I(HullMovingAverage, self.data.Close, self.hma_fast)
        self.hma2 = self.I(HullMovingAverage, self.data.Close, self.hma_slow)
        self.adx_value = self.I(
            ta.trend.adx,
            pd.Series(self.data.High),
            pd.Series(self.data.Low),
            pd.Series(self.data.Close),
            self.adx,
        )

    def next(self):
        if (
            not self.position
            and crossover(self.hma1, self.hma2)
            and self.adx_value > self.adx_threshold
        ):
            self.buy()
        elif self.position and crossover(self.hma2, self.hma1):
            self.position.close()
