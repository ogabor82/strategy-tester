# trading_backtest/main.py
from controllers.timeframe_set_controller import choose_timeframe_set
from controllers.ticker_set_controller import choose_tickers
from controllers.strategy_controller import choose_strategy
import backtest
from controllers.timeframe_set_controller import get_timeframe_sets
from controllers.strategy_controller import get_strategies
from controllers.optimization_controller import create_optimization_session
import optimization
from controllers.backtest_controller import create_session

from db.db import init_db, load_last_optimization_session, load_last_session

# Dictionary to store selected options
selected_options = {
    "timeframe_set": "None",  # Load the default configuration
    "tickers": ["AAPL"],
    "strategy": "None",
    "backtest_plot": True,
    "backtest_results": "compact",
    "selected_session": "None",
    "optimization_session": "None",
}


def main_menu():
    init_db()
    timeframe_sets = get_timeframe_sets()
    selected_options["timeframe_set"] = timeframe_sets[0]
    selected_options["selected_session"] = load_last_session()
    strategies = get_strategies()
    selected_options["strategy"] = strategies[0]
    selected_options["optimization_session"] = load_last_optimization_session()

    while True:
        import os

        os.system("cls" if os.name == "nt" else "clear")

        print("Current selections:")
        for key, value in selected_options.items():
            print(f"{key.capitalize()}: {value}")

        print("\nMain Menu:")
        print("1. Choose timeframe set")
        print("2. Choose tickers")
        print("3. Choose strategy")
        print("4. Backtest")
        print("5. Optimization")
        print("6. Create backtest session")
        print("7. Create optimization session")
        print("9. Exit")

        choice = input("Select an option (1-7): ")

        if choice == "1":
            selected_options["timeframe_set"] = (
                choose_timeframe_set.choose_timeframe_set()
            )
        elif choice == "2":
            selected_options["tickers"] = choose_tickers.choose_tickers()
        elif choice == "3":
            selected_options["strategy"] = choose_strategy.choose_strategy()
        elif choice == "4":
            backtest.run_backtest(selected_options)
            input("Press any key to continue...")
        elif choice == "5":
            optimization.optimize(selected_options)
            input("Press any key to continue...")
        elif choice == "6":
            create_session.create_session()
            input("Press any key to continue...")
            selected_options["selected_session"] = load_last_session()
        elif choice == "7":
            create_optimization_session.create_optimization_session()
            input("Press any key to continue...")
            selected_options["optimization_session"] = load_last_optimization_session()
        elif choice == "9":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()
