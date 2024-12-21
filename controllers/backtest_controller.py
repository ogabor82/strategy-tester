import sqlite3

DB = None


def init_db():
    global DB
    try:
        DB = sqlite3.connect("./strategy_tester.db")
        DB.row_factory = sqlite3.Row
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return e


def get_backtest_slices():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_slice")
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]
    return result


def get_backtest_session_stats(backtest_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        """
        SELECT 
            ticker,
            strategy.name as strategy_name,
            ROUND(AVG(return), 2) as avg_return,
            ROUND(AVG(buyhold_return), 2) as avg_buyhold_return,
            COUNT(*) as trade_count
        FROM backtest_slice
        LEFT JOIN strategy ON backtest_slice.strategy_id = strategy.id
        WHERE backtest_session_id = ?
        GROUP BY ticker, strategy_id
    """,
        (backtest_id,),
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_backtest_slices_by_session_id(backtest_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        """
        SELECT *, strategy.name as strategy_name
        FROM backtest_slice
        LEFT JOIN strategy ON backtest_slice.strategy_id = strategy.id
        WHERE backtest_slice.backtest_session_id = ?
    """,
        (backtest_id,),
    )
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]

    return result


def get_backtest_sessions():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_session")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_backtest_slices_by_strategy_id(strategy_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_slice WHERE strategy_id = ?", (strategy_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_backtest_sessions_by_project_id(project_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_session WHERE project_id = ?", (project_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
