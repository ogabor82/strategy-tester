def get_ticker_sets():
    ticker_sets = [
        {"name": "Tech Giants", "tickers": ["AAPL", "GOOGL", "MSFT", "AMZN"]},
        {"name": "FAANG", "tickers": ["META", "AAPL", "AMZN", "NFLX", "GOOGL"]},
        {"name": "Cryptocurrencies", "tickers": ["BTC-USD", "ETH-USD", "LTC-USD", "SOL-USD", "AVAX-USD"]},
        {"name": "Crypto top 25", "tickers": ["BTC-USD", "ETH-USD", "SOL-USD", "AVAX-USD", "LTC-USD", "DOGE-USD", "XRP-USD", "DOT1-USD", "SHIB-USD", "UNI3-USD", "LINK-USD", "BCH-USD", "MATIC-USD", "ALGO-USD", "ATOM1-USD", "ICP-USD", "FIL-USD", "ETC-USD", "TRX-USD", "XLM-USD", "VET-USD", "EOS-USD", "AAVE-USD", "XTZ-USD", "THETA-USD"]},
        {"name": "Forex Majors", "tickers": ["EURUSD=X", "JPY=X", "GBPUSD=X", "AUDUSD=X"]},
        {"name": "Commodities", "tickers": ["GC=F", "SI=F", "CL=F", "HG=F"]},
        {"name": "Indexes", "tickers": ["^GSPC", "^DJI", "^IXIC", "^RUT"]},
        {"name": "ETFs", "tickers": ["SPY", "QQQ", "DIA", "IWM"]},
        {"name": "Bonds", "tickers": ["IEF", "TLT", "SHY", "LQD"]},
        {"name": "Only BTC", "tickers": ["BTC-USD"]}
    ]   
    return ticker_sets