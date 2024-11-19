# trading_backtest/backtest.py
from strategies.SmaCrossAdx import SmaCrossAdx
from backtesting import Backtest
import yfinance as yf

from utils.results_extractor import extract_data

def run_backtest(strategy, tickers, configuration, backtest_plot, backtest_results):
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

        if backtest_results == "compact":
            result_data = extract_data(str(stats))
            print("-----------------------------")
            print("Ticker: ", ticker)
            print("Return [%]", result_data["Return [%]"])
            print("Buy & Hold Return [%]", result_data["Buy & Hold Return [%]"])
            print("Max. Drawdown [%]", result_data["Max. Drawdown [%]"])
            # print(result_data)
        elif backtest_results == "detailed":
            print(stats)
            print(stats._trades)
            print(stats._trades['pnl'].sum())
            print(stats._trades['duration'].mean())
            print(stats._trades['duration'].max())
            print(stats._trades['duration'].min())            
        if backtest_plot:    
            bt.plot()


    
