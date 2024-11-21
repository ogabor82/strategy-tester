import sqlite3

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
        "kelly_criterion" FLOAT
        );
        ''')        

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "configuration" (
        "id" INTEGER PRIMARY KEY,
        "name" VARCHAR,
        "start" DATETIME,
        "end" DATETIME,
        "interval" VARCHAR
        );
        ''')        

        # Create the "strategy" table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS "strategy" (
        "id" INTEGER PRIMARY KEY,
        "name" VARCHAR,
        "description" VARCHAR
        );
        ''')     

        # Add foreign key constraints
        cursor.execute('''
        ALTER TABLE "backtest_slice"
        ADD FOREIGN KEY ("configuration_id") REFERENCES "configuration" ("id");
        ''')

        cursor.execute('''
        ALTER TABLE "backtest_slice"
        ADD FOREIGN KEY ("strategy_id") REFERENCES "strategy" ("id");
        ''')

        cursor.execute('''
        ALTER TABLE "backtest_slice"
        ADD FOREIGN KEY ("backtest_session_id") REFERENCES "backtest_session" ("id");
        ''')           

        DB.commit()
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        return e
    
def load_last_session():
    global DB
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM backtest_session ORDER BY id DESC LIMIT 1")
    return cursor.fetchone()
