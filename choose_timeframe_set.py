from controllers.timeframe_set_controller import get_timeframe_sets

# trading_backtest/choose_configuration.py
def choose_timeframe_set():    
    timeframe_sets = get_timeframe_sets()

    print("Available timeframe sets:")
    for i, config in enumerate(timeframe_sets):
        print(f"{i + 1}: {config}")

    choice = int(input("Select a timeframe set by number: ")) - 1
    set_name = timeframe_sets[choice]
    print(f"Timeframe set selected: {set_name}")
    return set_name