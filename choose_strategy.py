# trading_backtest/choose_strategy.py
def choose_strategy():
    strategies = [
        {"name": "MaCross", "module": "ma_cross"},
        {"name": "SeriousMACD", "module": "serious_macd"},
    ]
    print("Choose a strategy:")
    for i, strategy in enumerate(strategies, start=1):
        print(f"{i}. {strategy}")
    choice = int(input("Enter the number of your chosen strategy: "))
    strategy = strategies[choice - 1]
    print(f"Strategy selected: {strategy}")
    return strategy