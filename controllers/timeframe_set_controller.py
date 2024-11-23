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
    
def get_timeframe_sets():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM timeframe_set")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_timeframes():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM timeframe")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]

def get_timeframes_by_timeframe_set_id(timeframe_set_id):
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM timeframe WHERE timeframe_set_id = ?", (timeframe_set_id,))
    rows = cursor.fetchall()
    return [dict(row) for row in rows]