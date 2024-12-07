backtest_sets_rsi_simple = [
    {"name": "default", "rsi_window": 14, "rsi_overbought": 70, "rsi_oversold": 30},
    {"name": "aggressive", "rsi_window": 14, "rsi_overbought": 65, "rsi_oversold": 35},
    {
        "name": "conservative",
        "rsi_window": 21,
        "rsi_overbought": 75,
        "rsi_oversold": 25,
    },
]

optimization_sets_rsi_simple = [
    {
        "name": "default",
        "config": {
            "maximize": "Equity Final [$]",
            "method": "grid",
            "max_tries": 1000,
            "random_state": 0,
            "return_heatmap": True,
        },
        "variables": {
            "rsi_window": {"from": 7, "to": 30, "step": 1},
            "rsi_overbought": {"from": 60, "to": 85, "step": 5},
            "rsi_oversold": {"from": 15, "to": 40, "step": 5},
        },
    }
]
