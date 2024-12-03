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
},
{
    "name": "adx",
    "config": {
        "maximize": "Equity Final [$]",
        "method": "grid",
        "max_tries": 1000,
        "random_state": 0,
        "return_heatmap": True
    },
    "variables": {
        "sma_fast": {
            "from": 10,
            "to": 80,
            "step": 1
        },        
        "adx": {
            "from": 1,
            "to": 100,
            "step": 1
        }
    }
}]
