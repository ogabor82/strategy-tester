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


def get_optimization_sessions():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM optimization_session")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_optimization_sessions_by_project_id(project_id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT * FROM optimization_session WHERE project_id = ?", (project_id,)
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_optimization_slices_by_session_id(id: int):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        """
        SELECT *, strategy.name as strategy_name
        FROM optimization_slice
        LEFT JOIN strategy ON optimization_slice.strategy_id = strategy.id
        WHERE optimization_slice.optimization_session_id = ?
    """,
        (id,),
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]
