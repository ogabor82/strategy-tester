# trading_backtest/main.py
import choose_configuration
import choose_tickers
import choose_strategy
import backtest
import optimization
import json

# Load configuration from JSON
def load_configuration():
    with open('configuration/configuration.json') as config_file:
        config_data = json.load(config_file)
    return config_data[0]  # Adjust as necessary

# Dictionary to store selected options
selected_options = {
    "configuration": load_configuration(),  # Load the default configuration
    "tickers": ["AAPL"],
    "strategy": ["MaCross"],
    "backtest_plot": False,
    "backtest_results": "compact"
}

def main_menu():
    while True:
        import os
        os.system('cls' if os.name == 'nt' else 'clear')

        print("Current selections:")
        for key, value in selected_options.items():
            print(f"{key.capitalize()}: {value}")

        print("\nMain Menu:")
        print("1. Choose configuration")
        print("2. Choose tickers")
        print("3. Choose strategy")
        print("4. Backtest")
        print("5. Optimization")
        print("6. Exit")


        choice = input("Select an option (1-7): ")

        if choice == '1':
            selected_options["configuration"] = choose_configuration.choose_config()
        elif choice == '2':
            selected_options["tickers"] = choose_tickers.choose_tickers()
        elif choice == '3':
            selected_options["strategy"] = choose_strategy.choose_strategy()
        elif choice == '4':
            backtest.run_backtest(selected_options["strategy"], 
                                  selected_options["tickers"], 
                                  selected_options["configuration"], 
                                  selected_options["backtest_plot"], 
                                  selected_options["backtest_results"]
                                  )
            input("Press any key to continue...")
        elif choice == '5':
            optimization.optimize(selected_options)        
        elif choice == '6':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()