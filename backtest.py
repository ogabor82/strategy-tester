# trading_backtest/backtest.py
from strategies.SmaCrossAdx import SmaCrossAdx
from backtesting import Backtest
import yfinance as yf

def run_backtest(strategy, tickers, configuration):
    print("Running backtest with the following options:")
    print(f"Strategy: {strategy}")
    print(f"Tickers: {tickers}")
    print(f"Configuration: {configuration}")
    # Here you can add logic to perform the backtest
    # using the selected strategy, tickers, and configuration

    TICKER = tickers[0]
    START_DATE = '2018-01-01'
    #START_DATE = '2023-01-01'
    END_DATE = '2024-03-12'
    FREQUENCY = '1d'

    for ticker in tickers:
        print(f"Running backtest for ticker: {ticker}")
        df_prices = yf.Ticker(ticker).history(start=START_DATE, end=END_DATE, interval=FREQUENCY)
        df_prices.index = df_prices.index.tz_localize(None)

        # bt = Backtest(df_prices, strategy, cash=10_000, commission=0, exclusive_orders=True)
        bt = Backtest(df_prices, SmaCrossAdx, cash=10_000, commission=0, exclusive_orders=True)
        stats = bt.run()        
        print(stats)
        # print(stats._trades)
        bt.plot()


    
