backtest_sets_serious_macd = [{
    "name": "default",
    "macd_a": 85,
    "macd_b": 80,
    "stoch_k": 70,
    "stoch_k_smoothing": 10,
    "stoch_d_smoothing": 3,
    "ema": 200,
    "sl": 0.82
}, {
    "name": "slow",
    "macd_a": 85,
    "macd_b": 80,
    "stoch_k": 70,
    "stoch_k_smoothing": 10,
    "stoch_d_smoothing": 3,
    "ema": 200,
    "sl": 0.82
}]

optimization_sets_serious_macd = [
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
            "macd_a": {
                "from": 5,
                "to": 100,
                "step": 5
            },
            "macd_b": {
                "from": 5,
                "to": 100,
                "step": 5
            },
            "stoch_k": {
                "from": 5,
                "to": 100,
                "step": 5
            },
            "ema": {
                "from": 5,
                "to": 500,
                "step": 5
            },
            
        }
    }
]