import json
import sqlite3
from controllers.timeframe_set_controller import get_timeframes_by_timeframe_set_id
from strategies.EmaCrossAdx.EmaCrossAdx import EmaCrossAdx
from strategies.RSISimple.RSISimple import RSISimple
from strategies.SeriousMACD.SeriousMACD import SeriousMACD
from strategies.SmaCrossAdx.SmaCrossAdx import SmaCrossAdx
from strategies.SuperTrend.SuperTrend import SuperTrend
from backtesting import Backtest

import seaborn as sns
from backtesting.lib import plot_heatmaps

from utils.data_conversion import convert_to_namedtuple
from utils.price_fetcher import get_price_data

DB = None


def init_db():
    global DB
    try:
        DB = sqlite3.connect("./strategy_tester.db")
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
    optimization_set = {
        key: value
        for key, value in selected_options["optimization_set"].items()
        if key != "name"
    }

    # New code to iterate through optimization_set["variables"]
    modified_optimization_set = {}
    param_keys = []
    for key, value in optimization_set.get("variables", {}).items():
        # Modify the value as needed
        modified_optimization_set[key] = range(
            value["from"], value["to"], value["step"]
        )
        param_keys.append(key)

    modified_optimization_set["maximize"] = optimization_set["config"]["maximize"]
    modified_optimization_set["method"] = optimization_set["config"]["method"]
    modified_optimization_set["max_tries"] = optimization_set["config"]["max_tries"]
    modified_optimization_set["random_state"] = optimization_set["config"][
        "random_state"
    ]
    modified_optimization_set["return_heatmap"] = optimization_set["config"][
        "return_heatmap"
    ]

    timeframes = selected_options["timeframe_set"]["timeframes"]

    START_DATE = timeframes[0]["start"]
    END_DATE = timeframes[0]["end"]
    FREQUENCY = timeframes[0]["interval"]

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

    print("Selected options:")
    print(selected_options)
    print("Optimization config:")
    print(modified_optimization_set)

    for ticker in selected_options["tickers"]:
        print(f"Running optimization for ticker: {ticker}")
        df_prices = get_price_data(ticker, START_DATE, END_DATE, FREQUENCY)

        bt = Backtest(
            df_prices, strategy, cash=100_000, commission=0, exclusive_orders=True
        )

        stats, heatmap = bt.optimize(**modified_optimization_set)

        optimization_results = {
            "best_params": {key: getattr(stats._strategy, key) for key in param_keys},
            "metrics": {
                "Return [%]": stats["Return [%]"],
                "Sharpe Ratio": stats["Sharpe Ratio"],
                "Max. Drawdown [%]": stats["Max. Drawdown [%]"],
                "Win Rate [%]": stats["Win Rate [%]"],
            },
        }

        opt_params = json.dumps(stats._strategy, default=str)
        opt_params_dict = json.loads(opt_params)
        opt_params_namedtuple = convert_to_namedtuple(opt_params_dict)

        optimization_results = {
            "best_params": {
                key: getattr(opt_params_namedtuple, key) for key in param_keys
            },
            "metrics": {
                "Return [%]": stats["Return [%]"],
                "Sharpe Ratio": stats["Sharpe Ratio"],
                "Max. Drawdown [%]": stats["Max. Drawdown [%]"],
                "Win Rate [%]": stats["Win Rate [%]"],
            },
        }

        filename = f"reports/optimization/optimization_results_{ticker}_{strategy_id}_{START_DATE}_{END_DATE}_{FREQUENCY}"

        cursor = DB.cursor()
        cursor.execute(
            """
            INSERT INTO optimization_slice (
                optimization_session_id,
                strategy_id,
                ticker,
                start,
                end,
                interval,
                optimization_results
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                selected_options["optimization_session"]["id"],
                strategy_id,
                ticker,
                START_DATE,
                END_DATE,
                FREQUENCY,
                json.dumps(optimization_results),
            ),
        )

        DB.commit()

        sns.heatmap(heatmap.unstack())
        if selected_options["backtest_plot"]:
            plot_heatmaps(heatmap, agg="mean", plot_width=1200, filename=filename)
