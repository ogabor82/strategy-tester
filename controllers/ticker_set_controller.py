def get_ticker_sets():
    ticker_sets = [
        {"name": "Tech Giants", "tickers": ["AAPL", "GOOGL", "MSFT", "AMZN"]},
        {"name": "FAANG", "tickers": ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]},
        {"name": "Cryptocurrencies", "tickers": ["BTCUSDT", "ETHUSDT", "LTCUSDT", "SOLUSDT", "AVAXUSDT"]},
        {"name": "Crypto top 25", "tickers": ["BTCUSDT", "ETHUSDT", "SOLUSDT", "AVAXUSDT", "LTCUSDT", "DOGEUSDT", "XRPUSDT", "DOT1USDT", "SHIBUSDT", "UNI3USDT", "LINKUSDT", "BCHUSDT", "MATICUSDT", "ALGOUSDT", "ATOM1USDT", "ICPUSDT", "FILUSDT", "ETCUSDT", "TRXUSDT", "XLMUSDT", "VETUSDT", "EOSUSDT", "AAVEUSDT", "XTZUSDT", "THETAUSDT"]},
        {"name": "Forex Majors", "tickers": ["EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X"]},
        {"name": "Commodities", "tickers": ["GC=F", "SI=F", "CL=F", "HG=F"]},
        {"name": "Indexes", "tickers": ["^GSPC", "^DJI", "^IXIC", "^RUT"]},
        {"name": "ETFs", "tickers": ["SPY", "QQQ", "DIA", "IWM"]},
        {"name": "Bonds", "tickers": ["IEF", "TLT", "SHY", "LQD"]},
        {"name": "Only BTC", "tickers": ["BTCUSDT"]}
    ]   
    return ticker_sets