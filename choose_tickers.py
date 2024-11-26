# trading_backtest/choose_tickers.py
from controllers.ticker_set_controller import get_ticker_sets

def choose_tickers():
    ticker_sets = get_ticker_sets()
    print("Choose a set of tickers:")
    for i, ticker_set in enumerate(ticker_sets, start=1):
        print(f"{i}. {ticker_set}")
    choice = int(input("Enter the number of your chosen ticker set: "))
    tickers = ticker_sets[choice - 1]["tickers"]
    print(f"Tickers selected: {tickers}")
    return tickers