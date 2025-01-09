# Seed data
import json

from strategies.SeriousMACD.SeriousMACD_db import (
    backtest_sets_serious_macd,
    optimization_sets_serious_macd,
)
from strategies.SmaCrossAdx.SmaCrossAdx_db import (
    backtest_sets_ma_cross_adx,
    optimization_sets_ma_cross_adx,
)
from strategies.SuperTrend.SuperTrend_db import (
    backtest_sets_super_trend,
    optimization_sets_super_trend,
)
from strategies.RSISimple.RSISimple_db import (
    backtest_sets_rsi_simple,
    optimization_sets_rsi_simple,
)
from strategies.EmaCrossAdx.EmaCrossAdx_db import (
    backtest_sets_ema_cross_adx,
    optimization_sets_ema_cross_adx,
)
from strategies.HullmaCrossAdx.HullmaCrossAdx_db import (
    backtest_sets_hma_cross_adx,
    optimization_sets_hma_cross_adx,
)

strategies = [
    (
        1,
        "MaCross",
        "Sample MaCross strategy with ADX",
        json.dumps(backtest_sets_ma_cross_adx),
        json.dumps(optimization_sets_ma_cross_adx),
    ),
    (
        2,
        "SeriousMACD",
        "SeriousMACD strategy from Serius Backtester youtube channel",
        json.dumps(backtest_sets_serious_macd),
        json.dumps(optimization_sets_serious_macd),
    ),
    (
        3,
        "SuperTrend",
        "SuperTrend strategy",
        json.dumps(backtest_sets_super_trend),
        json.dumps(optimization_sets_super_trend),
    ),
    (
        4,
        "RSISimple",
        "RSISimple strategy",
        json.dumps(backtest_sets_rsi_simple),
        json.dumps(optimization_sets_rsi_simple),
    ),
    (
        5,
        "EmaCrossAdx",
        "EmaCrossAdx strategy",
        json.dumps(backtest_sets_ema_cross_adx),
        json.dumps(optimization_sets_ema_cross_adx),
    ),
    (
        6,
        "HullmaCrossAdx",
        "HullmaCrossAdx strategy",
        json.dumps(backtest_sets_hma_cross_adx),
        json.dumps(optimization_sets_hma_cross_adx),
    ),
]

timeframe_sets = [
    (1, "default"),
    (2, "2020"),
    (3, "Pandemic"),
    (4, "Crypto bear market"),
    (5, "2023"),
    (6, "2024"),
    (7, "All BTC bull markets"),
    (8, "2024 1H 1D"),
    (9, "2024 15min"),
]

timeframes = [
    (1, 1, "default", "2018-01-01", "2024-03-12", "1d"),
    (2, 2, "2020", "2020-01-01", "2020-12-31", "1d"),
    (3, 3, "Pandemic", "2020-01-01", "2023-12-31", "1d"),
    (4, 4, "Crypto bear market 1D", "2021-11-01", "2022-12-31", "1d"),
    (5, 4, "Crypto bear market 1H", "2021-11-01", "2022-12-31", "1h"),
    (6, 5, "2023 1H", "2023-01-01", "2023-12-31", "1h"),
    (7, 6, "2024 1H", "2024-01-01", "2024-12-31", "1h"),
    (8, 7, "First BTC bull market", "2009-12-01", "2011-06-08", "1d"),
    (9, 7, "Second BTC bull market", "2012-01-01", "2013-12-10", "1d"),
    (10, 7, "Third BTC bull market", "2015-10-08", "2017-01-05", "1d"),
    (11, 7, "Fourth BTC bull market", "2019-02-08", "2021-09-07", "1d"),
    (12, 8, "2024 1H", "2024-01-01", "2024-12-31", "1h"),
    (13, 8, "2024 1D", "2024-01-01", "2024-12-31", "1d"),
    (14, 9, "2024 15min", "2024-10-10", "2024-12-05", "15m"),
]
