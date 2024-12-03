backtest_sets_super_trend = [{
    "name": "default",
    "min_adx": 14,
    "ema_window": 200
}, {
    "name": "slow",
    "min_adx": 20,
    "ema_window": 100
}, {
    "name": "fast",
    "min_adx": 14,
    "ema_window": 150
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
        },
        "variables": {
            "min_adx": {
                "from": 10,
                "to": 30,
                "step": 5
            },
            "ema_window": {
                "from": 50,
                "to": 250,
                "step": 5
            }
        }
    }
]