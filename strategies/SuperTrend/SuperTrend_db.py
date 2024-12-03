backtest_sets_super_trend = [{
    "name": "default",
    "atr_period": 10,
    "atr_multiplier": 3
}, {
    "name": "slow",
    "atr_period": 10,
    "atr_multiplier": 3
}]

optimization_sets_super_trend = [
    {
        "name": "default",
        "config": {
            "maximize": "Equity Final [$]",
            "method": "grid",
            "max_tries": 1000,
            "random_state": 0,
            "return_heatmap": True
        }
    }
]