import json
from controllers.timeframe_set_controller import get_timeframes_by_timeframe_set_id
import db.db
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
    print(f"Timeframe set: {selected_options['timeframe_set']}")
    
    timeframes = get_timeframes_by_timeframe_set_id(selected_options['timeframe_set']['id'])

    START_DATE = timeframes[0]["start"]
    END_DATE = timeframes[0]["end"]
    FREQUENCY = timeframes[0]["interval"]

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
    for i, opt_set in enumerate(optimization_sets):
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

        optimization_results = {
            "optimization_session_id": selected_options["optimization_session"][0],
            "strategy_id": strategy_id,
            "ticker": ticker,
            "sma_fast": int(stats._strategy.sma_fast),
            "sma_slow": int(stats._strategy.sma_slow)
        }


        filename = f"reports/optimization/optimization_results_{ticker}_{strategy_id}_{START_DATE}_{END_DATE}_{FREQUENCY}"        

        cursor = db.db.DB.cursor()
        cursor.execute("""
            INSERT INTO optimization_slice (
                optimization_session_id,
                strategy_id,
                ticker,
                start,
                end,
                interval,
                optimization_results
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            selected_options["optimization_session"][0], 
            strategy_id, 
            ticker, 
            START_DATE, 
            END_DATE, 
            FREQUENCY, 
            json.dumps(optimization_results)
        ))

        db.db.DB.commit()

        sns.heatmap(heatmap.unstack())
        if selected_options['backtest_plot']:            
            plot_heatmaps(heatmap, agg='mean', plot_width=1200, filename=filename)
