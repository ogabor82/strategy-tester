import json
import sqlite3
from controllers.timeframe_set_controller import get_timeframes_by_timeframe_set_id
from strategies.SeriousMACD.SeriousMACD import SeriousMACD
from strategies.SmaCrossAdx.SmaCrossAdx import SmaCrossAdx
from backtesting import Backtest
import yfinance as yf

import seaborn as sns
from backtesting.lib import plot_heatmaps

DB = None

def init_db():
    global DB
    try:
        DB = sqlite3.connect('./strategy_tester.db')
        DB.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return e

def run_optimization(selected_options):
    init_db()
    print("Running optimization with the following options:")
    print(f"Strategy: {selected_options['strategy']}")
    print(f"Tickers: {selected_options['tickers']}")
    print(f"Timeframe set: {selected_options['timeframe_set']}")
    optimization_set = {key: value for key, value in selected_options['optimization_set'].items() if key != 'name'}

    # New code to iterate through optimization_set["variables"]
    modified_optimization_set = {}
    for key, value in optimization_set.get("variables", {}).items():
        # Modify the value as needed
        modified_optimization_set[key] = range(value["from"], value["to"], value["step"])

    modified_optimization_set["maximize"] = optimization_set["config"]["maximize"]
    modified_optimization_set["method"] = optimization_set["config"]["method"]
    modified_optimization_set["max_tries"] = optimization_set["config"]["max_tries"]
    modified_optimization_set["random_state"] = optimization_set["config"]["random_state"]
    modified_optimization_set["return_heatmap"] = optimization_set["config"]["return_heatmap"]

    
    timeframes = get_timeframes_by_timeframe_set_id(selected_options['timeframe_set']['id'])

    START_DATE = timeframes[0]["start"]
    END_DATE = timeframes[0]["end"]
    FREQUENCY = timeframes[0]["interval"]

    if selected_options["strategy"]["name"] == "MaCross":
        strategy = SmaCrossAdx
        strategy_id = 1
    elif selected_options["strategy"]["name"] == "SeriousMACD":
        strategy = SeriousMACD
        strategy_id = 2    

    print("Selected options:")
    print(selected_options)     
    print("Optimization config:")
    print(modified_optimization_set)

    for ticker in selected_options['tickers']:
        print(f"Running optimization for ticker: {ticker}")
        df_prices = yf.Ticker(ticker).history(start=START_DATE, end=END_DATE, interval=FREQUENCY)
        df_prices.index = df_prices.index.tz_localize(None)
        
        bt = Backtest(df_prices, strategy, cash=100_000, commission=0, exclusive_orders=True)

        stats, heatmap = bt.optimize(**modified_optimization_set)
        
        print("Optimization results:")
        print("Optimal sma_fast:", stats._strategy.sma_fast)
        print("Optimal sma_slow:", stats._strategy.sma_slow)
        print("-----------------------------")

        optimization_results = {
            "sma_fast": int(stats._strategy.sma_fast),
            "sma_slow": int(stats._strategy.sma_slow)
        }


        filename = f"reports/optimization/optimization_results_{ticker}_{strategy_id}_{START_DATE}_{END_DATE}_{FREQUENCY}"        

        cursor = DB.cursor()
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
            selected_options["optimization_session"]["id"], 
            strategy_id, 
            ticker, 
            START_DATE, 
            END_DATE, 
            FREQUENCY, 
            json.dumps(optimization_results)
        ))

        DB.commit()

        sns.heatmap(heatmap.unstack())
        if selected_options['backtest_plot']:            
            plot_heatmaps(heatmap, agg='mean', plot_width=1200, filename=filename)
