# Seed data

import json

backtest_sets_ma_cross_adx = [{
    "name": "default",
    "sma_fast": 20,
    "sma_slow": 40,
    "adx": 14
}, {
    "name": "slow",
    "sma_fast": 20,
    "sma_slow": 80,
    "adx": 14
}]

optimization_sets_ma_cross_adx = [{
    "name": "rare fast",
    "config": {
        "maximize": "Equity Final [$]",
        "method": "grid",
        "max_tries": 1000,
        "random_state": 0,
        "return_heatmap": True
    },
    "variables": {
        "sma_fast": {
            "from": 5,
            "to": 60,
            "step": 5
        },
        "sma_slow": {
            "from": 20,
            "to": 100,
            "step": 5
        }
    }
}, {
    "name": "frequent slow",
    "config": {
        "maximize": "Equity Final [$]",
        "method": "grid",
        "max_tries": 1000,
        "random_state": 0,
        "return_heatmap": True
    },
    "variables": {
        "sma_fast": {
            "from": 1,
            "to": 80,
            "step": 1
        },
        "sma_slow": {
            "from": 10,
            "to": 80,
            "step": 5
        }
    }
}]


strategies = [
    (1, 'MaCross', 'Sample MaCross strategy with ADX', json.dumps(backtest_sets_ma_cross_adx), json.dumps(optimization_sets_ma_cross_adx)),
    (2, 'SeriousMACD', 'SeriousMACD strategy from Serius Backtester youtube channel', json.dumps(backtest_sets_ma_cross_adx), json.dumps(optimization_sets_ma_cross_adx)),
    (3, 'RSI', 'RSI strategy from Serius Backtester youtube channel', json.dumps(backtest_sets_ma_cross_adx), json.dumps(optimization_sets_ma_cross_adx))
]

timeframe_sets = [
    (1, 'default'),
    (2, '2020'),
    (3, 'Pandemic'),
    (4, 'Crypto bear market'),
    (5, '2023'),
    (6, '2024'),
    (7, 'All BTC bull markets'),
]

timeframes = [
    (1, 1, 'default', '2018-01-01', '2024-03-12', '1d'),
    (2, 2, '2020', '2020-01-01', '2020-12-31', '1d'),
    (3, 3, 'Pandemic', '2020-01-01', '2023-12-31', '1d'),
    (4, 4, 'Crypto bear market 1D', '2021-11-01', '2022-12-31', '1d'),
    (5, 4, 'Crypto bear market 1H', '2021-11-01', '2022-12-31', '1h'),
    (6, 5, '2023 1H', '2023-01-01', '2023-12-31', '1h'),
    (7, 6, '2024 1H', '2024-01-01', '2024-12-31', '1h'),
    (8, 7, 'First BTC bull market', '2009-12-01', '2011-06-08', '1d'),
    (9, 7, 'Second BTC bull market', '2012-01-01', '2013-12-10', '1d'),
    (10, 7, 'Third BTC bull market', '2015-10-08', '2017-01-05', '1d'),
    (11, 7, 'Fourth BTC bull market', '2019-02-08', '2021-09-07', '1d'), 
]

