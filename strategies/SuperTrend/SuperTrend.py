import pandas as pd
import numpy as np
from backtesting import Strategy
import ta

class SuperTrend(Strategy):
    # Strategy parameters
    atr_period = 10
    atr_multiplier = 3
    min_adx = 14
    ema_window = 200

    def init(self):
        # Calculate SuperTrend
        high = pd.Series(self.data.High)
        low = pd.Series(self.data.Low)
        close = pd.Series(self.data.Close)
        
        # Calculate ATR
        atr = ta.volatility.average_true_range(high, low, close, self.atr_period)
        
        # Calculate basic upper and lower bands
        hl2 = (high + low) / 2
        final_upperband = hl2 + (self.atr_multiplier * atr)
        final_lowerband = hl2 - (self.atr_multiplier * atr)
        
        # Initialize SuperTrend
        supertrend = pd.Series(index=close.index, dtype=float)
        direction = pd.Series(index=close.index, dtype=int)
        
        # Calculate SuperTrend values
        for i in range(1, len(close)):
            if close[i] > final_upperband[i-1]:
                direction[i] = 1
            elif close[i] < final_lowerband[i-1]:
                direction[i] = -1
            else:
                direction[i] = direction[i-1]
                
            if direction[i] == 1 and final_lowerband[i] < final_lowerband[i-1]:
                final_lowerband[i] = final_lowerband[i-1]
            if direction[i] == -1 and final_upperband[i] > final_upperband[i-1]:
                final_upperband[i] = final_upperband[i-1]
                
            if direction[i] == 1:
                supertrend[i] = final_lowerband[i]
            else:
                supertrend[i] = final_upperband[i]
        
        # Calculate 200 EMA
        ema_filter  = ta.trend.ema_indicator(close, window = self.ema_window)
        
        # Add ADX calculation
        adx = ta.trend.ADXIndicator(high, low, close, window=14)
        adx_value = adx.adx()
        
        # Store indicators for strategy use
        self.supertrend = self.I(lambda: supertrend)
        self.direction = self.I(lambda: direction)
        self.ema_filter = self.I(lambda: ema_filter)
        self.adx = self.I(lambda: adx_value)  # Add ADX to stored indicators
        
    def next(self):
        # If not in position and trend turns upward and price is above 200 EMA and ADX > 20, buy
        if (not self.position and 
            self.direction[-1] == 1 and 
            self.data.Close[-1] > self.ema_filter[-1] and
            self.adx[-1] > self.min_adx):  # Add ADX filter
            self.buy()
            
        # If in position and trend turns downward, sell
        elif self.position and self.direction[-1] == -1:
            self.position.close()
