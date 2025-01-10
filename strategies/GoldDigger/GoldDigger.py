import pandas as pd
import numpy as np
import ta
from backtesting import Strategy
from backtesting.lib import crossover


def EMA(closes: pd.Series, n: int) -> pd.Series:
    return pd.Series(closes).ewm(span=n, adjust=False).mean()


def SMA(values: pd.Series, n: int) -> pd.Series:
    return pd.Series(values).rolling(n).mean()


def KeltnerChannels(
    high: pd.Series, low: pd.Series, close: pd.Series, length: int, mult: float
):
    middle = SMA(close, length)
    range_ma = SMA(high - low, length)
    upper = middle + (range_ma * mult)
    lower = middle - (range_ma * mult)
    return upper, middle, lower


def DMI(high: pd.Series, low: pd.Series, close: pd.Series, length: int):
    # Convert inputs to pandas Series if they aren't already
    high = pd.Series(high)
    low = pd.Series(low)
    close = pd.Series(close)

    # Calculate +DI and -DI using ta-lib
    plus_di = ta.trend.adx_pos(high, low, close, window=length)
    minus_di = ta.trend.adx_neg(high, low, close, window=length)

    # Handle NaN values
    plus_di = plus_di.fillna(0)
    minus_di = minus_di.fillna(0)

    return plus_di, minus_di


class GoldDigger(Strategy):
    # Strategy parameters
    ribbon_period = 43  # Trend period
    keltner_length = 81  # Keltner channel length
    keltner_mult = 2.4  # Keltner channel multiplier
    dmi_length = 14  # DMI length
    dmi_threshold = 33  # DMI benchmark

    # Take profit and stop loss parameters
    tp1_level = 35  # Take profit level, 35 = 3.5%  !!!!
    tp1_qty = 100  # Take profit quantity percentage
    sl_level = 40  # Stop loss level, 40 = 4%  !!!!

    def init(self):
        # Trend indicators - EMA and SMA
        self.leadLine1 = self.I(EMA, self.data.Close, self.ribbon_period)
        self.leadLine2 = self.I(SMA, self.data.Close, self.ribbon_period)

        # Keltner Channels
        self.kc_upper, self.kc_middle, self.kc_lower = self.I(
            KeltnerChannels,
            self.data.High,
            self.data.Low,
            self.data.Close,
            self.keltner_length,
            self.keltner_mult,
        )

        # DMI Indicators - updated implementation
        plus_di, minus_di = DMI(
            self.data.High, self.data.Low, self.data.Close, self.dmi_length
        )
        self.plus_di = self.I(lambda: plus_di)
        self.minus_di = self.I(lambda: minus_di)

        # Volume condition - using array indexing instead of shift
        self.volume_increased = self.I(lambda: self.data.Volume > self.data.Volume[-1])

    def next(self):
        price = self.data.Close[-1]

        # Entry conditions
        if (
            not self.position
            and self.leadLine2[-1] < self.leadLine1[-1]  # Upward trend
            and self.data.Open[-1] > self.kc_lower[-1]  # Price above lower Keltner
            and self.data.Open[-1] < self.kc_upper[-1]  # Price below upper Keltner
            and self.data.Close[-1] > self.kc_upper[-1]  # Close above upper Keltner
            and self.plus_di[-1] > self.minus_di[-1]  # Positive DMI crossover
            and self.plus_di[-1] > self.dmi_threshold  # DMI above threshold
            and self.volume_increased[-1]  # Volume increased
        ):
            # Calculate stop loss and take profit levels
            sl = price * (1 - self.sl_level / 1000)
            tp = price * (1 + self.tp1_level / 1000)

            # Open position with SL and TP
            self.buy(sl=sl, tp=tp)

        # Check for trailing stop using Keltner lower band
        if self.position and price < self.kc_lower[-1]:
            self.position.close()
