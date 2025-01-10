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


def get_strategies():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM strategy")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def create_strategy(name: str, description: str):
    print(name, description)
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        "INSERT INTO strategy (name, description) VALUES (?, ?)", (name, description)
    )
    DB.commit()
    return cursor.lastrowid


def choose_strategy():
    strategies = [
        {"name": "MaCross", "module": "ma_cross"},
        {"name": "SeriousMACD", "module": "serious_macd"},
    ]
    print("Choose a strategy:")
    for i, strategy in enumerate(strategies, start=1):
        print(f"{i}. {strategy}")
    choice = int(input("Enter the number of your chosen strategy: "))
    strategy = strategies[choice - 1]
    print(f"Strategy selected: {strategy}")
    return strategy
