import pandas as pd
import ta

from backtesting import Strategy
from backtesting.lib import crossover

class SeriousMACD(Strategy):
    macd_a = 85
    macd_b = 80

    stoch_k = 70
    stoch_k_smoothing = 10
    stoch_d_smoothing = 3

    ema = 200

    sl = 0.82

    def init(self):
        self.macd = self.I(ta.trend.macd, pd.Series(self.data.Close), self.macd_a, self.macd_b)
        self.signal = self.I(ta.trend.macd_signal, pd.Series(self.data.Close), self.macd_a, self.macd_b)
        
        self.stoch_k = self.I(ta.momentum.stochrsi_k, pd.Series(self.data.Close), self.stoch_k, self.stoch_k_smoothing, self.stoch_d_smoothing)

        self.ema = self.I(ta.trend.ema_indicator , pd.Series(self.data.Close), self.ema)

    def next(self):
        c1 = crossover(self.macd, self.signal)
        c1b = self.macd < 0 and self.signal < 0
        c2 = self.stoch_k < 35
        c3 = self.data.Close < self.ema

        e1 = crossover(self.signal, self.macd)
        e2 = self.macd > 0 and self.signal > 0
        e3 = self.stoch_k > 65

        price = self.data.Close[-1]

        if c1 and c1b and c2 and c3:
            self.buy(sl=self.sl * price)
            # self.buy()
        elif e1 and e2 and e3:
            self.position.close()