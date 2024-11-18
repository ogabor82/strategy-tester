import pandas as pd
import ta

from backtesting import Strategy
from backtesting.lib import crossover
import pandas as pd

def MovingAverage(closes:pd.Series, n:int) -> pd.Series:
    return pd.Series(closes).rolling(n).mean()

class SmaCrossAdx(Strategy):
    sma_fast = 20
    sma_slow = 25
    adx = 14
    
    def init(self):
        self.sma1 = self.I(MovingAverage, self.data.Close, self.sma_fast)
        self.sma2 = self.I(MovingAverage, self.data.Close, self.sma_slow)
        self.adx_value = self.I(ta.trend.adx, pd.Series(self.data.High), pd.Series(self.data.Low), pd.Series(self.data.Close), self.adx)

    def next(self):
        if not self.position and crossover(self.sma1, self.sma2) and self.adx_value > self.adx:
            self.buy()
        elif self.position and crossover(self.sma2, self.sma1):
            self.position.close()
         