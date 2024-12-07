import pandas as pd
import ta

from backtesting import Strategy


class RSISimple(Strategy):
    # Strategy parameters
    rsi_window = 14
    rsi_overbought = 70
    rsi_oversold = 30

    def init(self):
        # Calculate RSI
        close = pd.Series(self.data.Close)
        self.rsi = self.I(ta.momentum.rsi, close, self.rsi_window)

    def next(self):
        # If not in position and RSI crosses below oversold level, buy
        if not self.position and self.rsi[-1] < self.rsi_oversold:
            self.buy()

        # If in position and RSI crosses above overbought level, sell
        elif self.position and self.rsi[-1] > self.rsi_overbought:
            self.position.close()
