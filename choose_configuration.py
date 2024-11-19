import json

# trading_backtest/choose_configuration.py
def choose_config():
    with open('./configuration/configuration.json', 'r') as file:
        configurations = json.load(file)

    print("Available configurations:")
    for i, config in enumerate(configurations):
        print(f"{i + 1}: {config}")

    choice = int(input("Select a configuration by number: ")) - 1
    config_name = configurations[choice]
    print(f"Configuration selected: {config_name}")
    return config_name