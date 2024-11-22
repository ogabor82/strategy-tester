optimization_sets = [{
    "name": "rare fast",
    "sma_fast": range(5, 60, 5),
    "sma_slow": range(20, 100, 5),
    "maximize": "Equity Final [$]",
    "method": "grid",
    "max_tries": 1000,
    "random_state": 0,
    "return_heatmap": True
}, {
    "name": "frequent slow",
    "sma_fast": range(1, 30, 1),
    "sma_slow": range(10, 80, 5),
    "maximize": "Equity Final [$]",
    "method": "grid",
    "max_tries": 1000,
    "random_state": 0,
    "return_heatmap": True
}]