backtest_sets_ema_cross_adx = [
    {"name": "default", "ema_fast": 20, "ema_slow": 40, "adx": 14},
    {"name": "slow", "ema_fast": 20, "ema_slow": 80, "adx": 14},
]

optimization_sets_ema_cross_adx = [
    {
        "name": "rare fast",
        "config": {
            "maximize": "Equity Final [$]",
            "method": "grid",
            "max_tries": 1000,
            "random_state": 0,
            "return_heatmap": True,
        },
        "variables": {
            "ema_fast": {"from": 5, "to": 60, "step": 5},
            "ema_slow": {"from": 20, "to": 100, "step": 5},
        },
    },
    {
        "name": "frequent slow",
        "config": {
            "maximize": "Equity Final [$]",
            "method": "grid",
            "max_tries": 1000,
            "random_state": 0,
            "return_heatmap": True,
        },
        "variables": {
            "ema_fast": {"from": 1, "to": 80, "step": 1},
            "ema_slow": {"from": 10, "to": 80, "step": 5},
        },
    },
    {
        "name": "adx",
        "config": {
            "maximize": "Equity Final [$]",
            "method": "grid",
            "max_tries": 1000,
            "random_state": 0,
            "return_heatmap": True,
        },
        "variables": {
            "ema_fast": {"from": 10, "to": 80, "step": 1},
            "adx": {"from": 1, "to": 100, "step": 1},
        },
    },
]
