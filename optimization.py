from strategies.SmaCrossAdx import SmaCrossAdx
from backtesting import Backtest
import yfinance as yf

import seaborn as sns
from backtesting.lib import plot_heatmaps

def optimize(selected_options):
    print("Running optimization with the following options:")
    print(f"Strategy: {selected_options['strategy']}")
    print(f"Tickers: {selected_options['tickers']}")
    print(f"Configuration: {selected_options['configuration']}")
    

    START_DATE = selected_options['configuration']["start_date"]
    END_DATE = selected_options['configuration']["end_date"]
    FREQUENCY = selected_options['configuration']["interval"]

    for ticker in selected_options['tickers']:
        print(f"Running optimization for ticker: {ticker}")
        df_prices = yf.Ticker(ticker).history(start=START_DATE, end=END_DATE, interval=FREQUENCY)
        df_prices.index = df_prices.index.tz_localize(None)
        

        bt = Backtest(df_prices, SmaCrossAdx, cash=10_000, commission=0, exclusive_orders=True)

        stats, heatmap = bt.optimize(
            sma_fast=range(5, 60, 5),
            sma_slow=range(20, 100, 5),
            # constraint=lambda p: p.n_high > p.n_low,
            maximize='Equity Final [$]',
            method = 'grid',
            max_tries=1000,
            random_state=0,
            return_heatmap=True)
        
        print("Optimization results:")
        print("Optimal sma_fast:", stats._strategy.sma_fast)
        print("Optimal sma_slow:", stats._strategy.sma_slow)
        print("-----------------------------")

        sns.heatmap(heatmap.unstack())
        if selected_options['backtest_plot']:            
            plot_heatmaps(heatmap, agg='mean')
