# trading_backtest/backtest.py
import json
import sqlite3
import uuid
from strategies.EmaCrossAdx.EmaCrossAdx import EmaCrossAdx
from strategies.SmaCrossAdx.SmaCrossAdx import SmaCrossAdx
from strategies.SeriousMACD.SeriousMACD import SeriousMACD
from strategies.SuperTrend.SuperTrend import SuperTrend
from strategies.RSISimple.RSISimple import RSISimple
from strategies.HullmaCrossAdx.HullmaCrossAdx import HullmaCrossAdx
from strategies.GoldDigger.GoldDigger import GoldDigger
from backtesting import Backtest
from utils.price_fetcher import get_price_data
from utils.results_extractor import extract_data

DB = None


def init_db():
    global DB
    try:
        DB = sqlite3.connect("./strategy_tester.db")
        DB.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return e


def run_backtest(selected_options):
    init_db()
    print("Running backtest with the following options:")
    print(f"Strategy: {selected_options['strategy']}")
    print(f"Tickers: {selected_options['tickers']}")
    print(f"Timeframe set: {selected_options['timeframe_set']}")
    print(f"Backtest set: {selected_options['backtest_set']}")
    backtest_set = {
        key: value
        for key, value in selected_options["backtest_set"].items()
        if key != "name"
    }

    timeframes = selected_options["timeframe_set"]["timeframes"]
    print(timeframes)

    if selected_options["strategy"]["name"] == "MaCross":
        strategy = SmaCrossAdx
        strategy_id = 1
    elif selected_options["strategy"]["name"] == "SeriousMACD":
        strategy = SeriousMACD
        strategy_id = 2
    elif selected_options["strategy"]["name"] == "SuperTrend":
        strategy = SuperTrend
        strategy_id = 3
    elif selected_options["strategy"]["name"] == "RSISimple":
        strategy = RSISimple
        strategy_id = 4
    elif selected_options["strategy"]["name"] == "EmaCrossAdx":
        strategy = EmaCrossAdx
        strategy_id = 5
    elif selected_options["strategy"]["name"] == "HullMaCrossAdx":
        strategy = HullmaCrossAdx
        strategy_id = 6
    elif selected_options["strategy"]["name"] == "GoldDigger":
        strategy = GoldDigger
        strategy_id = 7

    for timeframe in timeframes:
        START_DATE = timeframe["start"]
        END_DATE = timeframe["end"]
        FREQUENCY = timeframe["interval"]

        for ticker in selected_options["tickers"]:
            print(f"Running backtest for ticker: {ticker}")

            df_prices = get_price_data(ticker, START_DATE, END_DATE, FREQUENCY)

            bt = Backtest(
                df_prices, strategy, cash=100_000, commission=0, exclusive_orders=True
            )
            stats = bt.run(**backtest_set)

            filename = f"reports/backtest/backtest_results_{uuid.uuid4()}"

            if selected_options["backtest_results"] == "compact":
                print(stats)
                print(stats._trades)
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

                cursor = DB.cursor()
                cursor.execute(
                    """
                    INSERT INTO backtest_slice (
                        backtest_session_id,
                        configuration_id,
                        strategy_id,
                        strategy_parameters,
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
                        kelly_criterion,
                        filename
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )
                """,
                    (
                        selected_options["selected_session"]["id"],
                        selected_options["timeframe_set"]["name"],
                        strategy_id,
                        json.dumps(backtest_set),
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
                        result_data["Kelly Criterion"],
                        filename,
                    ),
                )

                DB.commit()

                # print(result_data)
            elif selected_options["backtest_results"] == "detailed":
                print(stats)
                # print(stats._trades)
            if selected_options["backtest_plot"]:
                bt.plot(filename=filename, open_browser=False)
