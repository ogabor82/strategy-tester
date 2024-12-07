import pandas as pd
import ta

from backtesting import Strategy
from backtesting.lib import crossover


def ExponentialMovingAverage(closes: pd.Series, n: int) -> pd.Series:
    return pd.Series(closes).ewm(span=n, adjust=False).mean()


class EmaCrossAdx(Strategy):
    ema_fast = 20
    ema_slow = 40
    adx = 14

    def init(self):
        self.ema1 = self.I(ExponentialMovingAverage, self.data.Close, self.ema_fast)
        self.ema2 = self.I(ExponentialMovingAverage, self.data.Close, self.ema_slow)
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
            and crossover(self.ema1, self.ema2)
            and self.adx_value > self.adx
        ):
            self.buy()
        elif self.position and crossover(self.ema2, self.ema1):
            self.position.close()
