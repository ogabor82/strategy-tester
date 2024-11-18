# trading_backtest/choose_strategy.py
def choose_strategy():
    strategies = ["Mean Reversion", "Trend Following", "Statistical Arbitrage"]
    print("Choose a strategy:")
    for i, strategy in enumerate(strategies, start=1):
        print(f"{i}. {strategy}")
    choice = int(input("Enter the number of your chosen strategy: "))
    strategy_name = strategies[choice - 1]
    print(f"Strategy selected: {strategy_name}")
    return strategy_name