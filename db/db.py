import sqlite3
from db.db_seed import strategies, timeframe_sets, timeframes

DB = None

def init_db():
    global DB
    try:
        DB = sqlite3.connect('./strategy_tester.db')
        create_tables()
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return e

def create_tables():
    if DB is None:
        print("Database connection is not established.")
        return

    try:
        cursor = DB.cursor()
        
        # Create the "backtest_session" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "backtest_session" (
        "id" INTEGER PRIMARY KEY,
        "name" VARCHAR,
        "details" VARCHAR
        );
        ''')

        # Create the "backtest_slice" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "backtest_slice" (
        "id" INTEGER PRIMARY KEY,
        "backtest_session_id" INTEGER,
        "configuration_id" INTEGER,
        "strategy_id" INTEGER,
        "ticker" VARCHAR,
        "start" DATETIME,
        "end" DATETIME,
        "interval" VARCHAR,
        "return" FLOAT,
        "buyhold_return" FLOAT,
        "max_drawdown" FLOAT,
        "trades" INTEGER,
        "win_rate" FLOAT,
        "sharpe_ratio" FLOAT,
        "kelly_criterion" FLOAT,
        "filename" VARCHAR
        );
        ''')       


        # Create the "optimization_session" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "optimization_session" (
        "id" INTEGER PRIMARY KEY,
        "name" VARCHAR,
        "details" VARCHAR
        );
        ''')

        # Create the "optimization_slice" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "optimization_slice" (
        "id" INTEGER PRIMARY KEY,
        "optimization_session_id" INTEGER,
        "timeframe_id" INTEGER,
        "strategy_id" INTEGER,
        "ticker" VARCHAR,
        "start" DATETIME,
        "end" DATETIME,
        "interval" VARCHAR,
        "optimization_results" VARCHAR
        );
        ''')

        # Create the "timeframe_set" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "timeframe_set" (
        "id" INTEGER PRIMARY KEY,
        "name" VARCHAR
        );
        ''')

        # Insert seed data into the timeframe_set table
        cursor.executemany('''
        INSERT INTO timeframe_set (id, name) VALUES (?, ?)
        ''', timeframe_sets)

        # Create the "timeframe" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "timeframe" (
        "id" INTEGER PRIMARY KEY,
        "timeframe_set_id" INTEGER,
        "name" VARCHAR,
        "start" DATETIME,
        "end" DATETIME,
        "interval" VARCHAR
        );
        ''')

        # Insert seed data into the timeframe table
        cursor.executemany('''
        INSERT INTO timeframe (id, timeframe_set_id, name, start, end, interval) VALUES (?, ?, ?, ?, ?, ?)
        ''', timeframes)


        # Create the "strategy" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "strategy" (
        "id" INTEGER PRIMARY KEY,
        "name" VARCHAR,
        "description" VARCHAR
        );
        ''')     

        # Insert seed data into the strategy table
        cursor.executemany('''
        INSERT INTO strategy (id, name, description) VALUES (?, ?, ?)
        ''', strategies)   

        DB.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        return e
    
def load_last_session():
    global DB
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_session ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()

def load_last_optimization_session():
    global DB
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM optimization_session ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()