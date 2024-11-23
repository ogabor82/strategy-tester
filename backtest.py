# trading_backtest/backtest.py
from strategies.SmaCrossAdx.SmaCrossAdx import SmaCrossAdx
from strategies.SeriousMACD.SeriousMACD import SeriousMACD
from backtesting import Backtest
import yfinance as yf
from controllers.timeframe_set_controller import get_timeframes_by_timeframe_set_id

from utils.results_extractor import extract_data
import db.db

def run_backtest(selected_options):
    print("Running backtest with the following options:")
    print(f"Strategy: {selected_options['strategy']}")
    print(f"Tickers: {selected_options['tickers']}")
    print(f"Timeframe set: {selected_options['timeframe_set']}")    

    timeframes = get_timeframes_by_timeframe_set_id(selected_options["timeframe_set"]["id"])

    START_DATE = timeframes[0]["start"]
    END_DATE = timeframes[0]["end"]
    FREQUENCY = timeframes[0]["interval"]

    if selected_options["strategy"]["name"] == "MaCross":
        strategy = SmaCrossAdx
        strategy_id = 1
    elif selected_options["strategy"]["name"] == "SeriousMACD":
        strategy = SeriousMACD
        strategy_id = 2


    for ticker in selected_options["tickers"]:
        print(f"Running backtest for ticker: {ticker}")
        df_prices = yf.Ticker(ticker).history(start=START_DATE, end=END_DATE, interval=FREQUENCY)
        df_prices.index = df_prices.index.tz_localize(None)

        bt = Backtest(df_prices, strategy, cash=100_000, commission=0, exclusive_orders=True)        
        stats = bt.run()        

        if selected_options["backtest_results"] == "compact":
            result_data = extract_data(str(stats))
            print("-----------------------------")
            print("Ticker: ", ticker)
            print("Return [%]", result_data["Return [%]"])
            print("Buy & Hold Return [%]", result_data["Buy & Hold Return [%]"])
            print("Max. Drawdown [%]", result_data["Max. Drawdown [%]"])
            print("# Trades", result_data["# Trades"])
            print("Win Rate [%]", result_data["Win Rate [%]"])
            print("Sharpe Ratio", result_data["Sharpe Ratio"])       
            print("Kelly Criterion", result_data["Kelly Criterion"])
      
            cursor = db.db.DB.cursor()
            cursor.execute("""
                INSERT INTO backtest_slice (
                    backtest_session_id,
                    configuration_id,
                    strategy_id,
                    ticker,
                    start,
                    end,
                    interval,
                    return,
                    buyhold_return,
                    max_drawdown,
                    trades,
                    win_rate,
                    sharpe_ratio,
                    kelly_criterion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                selected_options["selected_session"][0],
                selected_options["timeframe_set"]["name"],
                strategy_id,
                ticker,
                START_DATE,
                END_DATE,
                FREQUENCY,
                result_data["Return [%]"],
                result_data["Buy & Hold Return [%]"],
                result_data["Max. Drawdown [%]"],
                result_data["# Trades"],
                result_data["Win Rate [%]"],
                result_data["Sharpe Ratio"],
                result_data["Kelly Criterion"]
            ))

            db.db.DB.commit()
            
            # print(result_data)
        elif selected_options["backtest_results"] == "detailed":
            print(stats)
            # print(stats._trades)           
        if selected_options["backtest_plot"]:    
            bt.plot()


    
