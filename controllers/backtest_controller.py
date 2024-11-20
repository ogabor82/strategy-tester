import sqlite3

DB = None

def init_db():
    global DB
    try:
        DB = sqlite3.connect('./strategy_tester.db')
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

def get_backtest_slices_by_session_id(backtest_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute("""
        SELECT * FROM backtest_slice WHERE backtest_session_id = ?
    """, (backtest_id,))
    rows = cursor.fetchall()
    result = [dict(row) for row in rows]

    return result

def get_backtest_sessions():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_session")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_backtest_slices_by_session_id(session_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_slice WHERE backtest_session_id = ?", (session_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_strategies():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM strategy")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_backtest_slices_by_strategy_id(strategy_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_slice WHERE strategy_id = ?", (strategy_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
