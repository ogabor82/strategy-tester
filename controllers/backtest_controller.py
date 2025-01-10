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


def get_user_inputs():
    session_name = input("Enter the backtest session name: ")
    session_details = input("Enter the backtest session details: ")
    return session_name, session_details


def save_session(session_name, session_details, project_id):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        "INSERT INTO backtest_session (name, details, project_id) VALUES (?, ?, ?)",
        (session_name, session_details, project_id),
    )
    DB.commit()

    # Fetch the newly added record
    cursor.execute("SELECT * FROM backtest_session WHERE id = ?", (cursor.lastrowid,))
    new_record = cursor.fetchone()

    return new_record  # Return the newly added record


def create_session():
    session_name, session_details = get_user_inputs()
    print(f"Creating backtest session with name: {session_name}")
    print(f"Details: {session_details}")

    save_session(session_name, session_details)

    print("Backtest session created successfully.")


def delete_backtest_session(id):
    init_db()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM backtest_session WHERE id = ?", (id,))
    cursor.execute("DELETE FROM backtest_slice WHERE backtest_session_id = ?", (id,))
    DB.commit()
