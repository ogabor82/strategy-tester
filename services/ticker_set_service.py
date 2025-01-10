def get_ticker_sets():
    ticker_sets = [
        {"name": "Tech Giants", "tickers": ["AAPL", "GOOGL", "MSFT", "AMZN"]},
        {"name": "FAANG", "tickers": ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]},
        {"name": "Tech Xtreme", "tickers": ["TSLA", "NVDA", "AMD", "ASML"]},
        {
            "name": "Cryptocurrencies",
            "tickers": ["BTCUSDT", "ETHUSDT", "LTCUSDT", "SOLUSDT", "AVAXUSDT"],
        },
        {
            "name": "Crypto blue chips",
            "tickers": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT"],
        },
        {
            "name": "Crypto blue chips USDC",
            "tickers": ["BTCUSDC", "ETHUSDC", "SOLUSDC", "AVAXUSDC"],
        },
        {
            "name": "Crypto exotics",
            "tickers": ["DOGEUSDT", "XRPUSDT", "SHIBUSDT", "ADAUSDT", "BNBUSDT"],
        },
        {
            "name": "Crypto very exotic",
            "tickers": [
                "GALAUSDT",
                "NEARUSDT",
                "SUIUSDT",
                "AAVEUSDT",
                "PENDLEUSDT",
                "FETUSDT",
                "BICOUSDT",
            ],
        },
        {
            "name": "Crypto top 25",
            "tickers": [
                "BTCUSDT",
                "ETHUSDT",
                "SOLUSDT",
                "AVAXUSDT",
                "LTCUSDT",
                "DOGEUSDT",
                "XRPUSDT",
                "DOTUSDT",
                "SHIBUSDT",
                "UNI3USDT",
                "LINKUSDT",
                "BCHUSDT",
                "MATICUSDT",
                "ALGOUSDT",
                "ATOMUSDT",
                "ICPUSDT",
                "FILUSDT",
                "ETCUSDT",
                "TRXUSDT",
                "XLMUSDT",
                "VETUSDT",
                "EOSUSDT",
                "AAVEUSDT",
                "XTZUSDT",
                "THETAUSDT",
            ],
        },
        {
            "name": "Forex Majors",
            "tickers": ["EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X"],
        },
        {"name": "Commodities", "tickers": ["GC=F", "SI=F", "CL=F", "HG=F"]},
        {"name": "Indexes", "tickers": ["^GSPC", "^DJI", "^IXIC", "^RUT"]},
        {"name": "ETFs", "tickers": ["SPY", "QQQ", "DIA", "IWM"]},
        {"name": "Bonds", "tickers": ["IEF", "TLT", "SHY", "LQD"]},
        {"name": "Only BTC", "tickers": ["BTCUSDT"]},
    ]
    return ticker_sets


def choose_tickers():
    ticker_sets = get_ticker_sets()
    print("Choose a set of tickers:")
    for i, ticker_set in enumerate(ticker_sets, start=1):
        print(f"{i}. {ticker_set}")
    choice = int(input("Enter the number of your chosen ticker set: "))
    tickers = ticker_sets[choice - 1]["tickers"]
    print(f"Tickers selected: {tickers}")
    return tickers
