from strategies.SeriousMACD.SeriousMACD import SeriousMACD
from strategies.SmaCrossAdx.SmaCrossAdx import SmaCrossAdx
from backtesting import Backtest
import yfinance as yf

from strategies.SmaCrossAdx.SmaCrossAdxSets import optimization_sets as SmaCrossAdxSets
# from strategies.SeriousMACD.SeriousMACDSets import optimization_sets as SeriousMACDSets


import seaborn as sns
from backtesting.lib import plot_heatmaps

def optimize(selected_options):
    print("Running optimization with the following options:")
    print(f"Strategy: {selected_options['strategy']}")
    print(f"Tickers: {selected_options['tickers']}")
    print(f"Configuration: {selected_options['configuration']}")
    

    START_DATE = selected_options['configuration']["start"]
    END_DATE = selected_options['configuration']["end"]
    FREQUENCY = selected_options['configuration']["interval"]

    if selected_options["strategy"]["name"] == "MaCross":
        strategy = SmaCrossAdx
        optimization_sets = SmaCrossAdxSets[0]
        strategy_id = 1
    elif selected_options["strategy"]["name"] == "SeriousMACD":
        strategy = SeriousMACD
        # TODO: Change this to SeriousMACDSets
        optimization_sets = SmaCrossAdxSets[0] 
        strategy_id = 2    

    print("Available optimization sets:")
    for i, opt_set in enumerate(SmaCrossAdxSets):
        print(f"{i}: {opt_set}")

    selected_set_index = int(input("Select an optimization set by index: "))
    optimization_set = SmaCrossAdxSets[selected_set_index]

    for ticker in selected_options['tickers']:
        print(f"Running optimization for ticker: {ticker}")
        df_prices = yf.Ticker(ticker).history(start=START_DATE, end=END_DATE, interval=FREQUENCY)
        df_prices.index = df_prices.index.tz_localize(None)
        
        bt = Backtest(df_prices, SmaCrossAdx, cash=100_000, commission=0, exclusive_orders=True)

        stats, heatmap = bt.optimize(
            sma_fast = optimization_set['sma_fast'],
            sma_slow = optimization_set['sma_slow'],
            # constraint=lambda p: p.n_high > p.n_low,
            maximize = optimization_set['maximize'],
            method = optimization_set['method'],
            max_tries = optimization_set['max_tries'],
            random_state = optimization_set['random_state'],
            return_heatmap = optimization_set['return_heatmap']
            )
        
        print("Optimization results:")
        print("Optimal sma_fast:", stats._strategy.sma_fast)
        print("Optimal sma_slow:", stats._strategy.sma_slow)
        print("-----------------------------")

        sns.heatmap(heatmap.unstack())
        if selected_options['backtest_plot']:            
            plot_heatmaps(heatmap, agg='mean')
