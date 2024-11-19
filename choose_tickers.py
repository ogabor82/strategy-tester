# trading_backtest/choose_tickers.py
def choose_tickers():
    ticker_sets = [
        {"name": "Tech Giants", "tickers": ["AAPL", "GOOGL", "MSFT", "AMZN"]},
        {"name": "FAANG", "tickers": ["FB", "AAPL", "AMZN", "NFLX", "GOOGL"]},
        {"name": "Cryptocurrencies", "tickers": ["BTC-USD", "ETH-USD", "LTC-USD"]},
        {"name": "Forex Majors", "tickers": ["EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X"]},
        {"name": "Commodities", "tickers": ["GC=F", "SI=F", "CL=F", "HG=F"]},
        {"name": "Indexes", "tickers": ["^GSPC", "^DJI", "^IXIC", "^RUT"]},
        {"name": "ETFs", "tickers": ["SPY", "QQQ", "DIA", "IWM"]},
        {"name": "Bonds", "tickers": ["IEF", "TLT", "SHY", "LQD"]},
    ]
    print("Choose a set of tickers:")
    for i, ticker_set in enumerate(ticker_sets, start=1):
        print(f"{i}. {ticker_set}")
    choice = int(input("Enter the number of your chosen ticker set: "))
    tickers = ticker_sets[choice - 1]["tickers"]
    print(f"Tickers selected: {tickers}")
    return tickers