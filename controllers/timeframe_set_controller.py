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


def get_timeframe_sets():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM timeframe_set")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_timeframe_sets_with_timeframes():
    init_db()
    cursor = DB.cursor()
    cursor.execute("""
                   SELECT 
                       timeframe_set.id as timeframe_set_id, 
                       timeframe_set.name as timeframe_set_name,
                       timeframe.id as timeframe_id,
                       timeframe.name as timeframe_name,
                       timeframe.start as timeframe_start,
                       timeframe.end as timeframe_end,
                       timeframe.interval as timeframe_interval
                   FROM timeframe_set LEFT JOIN timeframe ON timeframe_set.id = timeframe.timeframe_set_id
                   """)
    rows = cursor.fetchall()
    timeframe_sets = {}
    for row in rows:
        timeframe_set_id = row["timeframe_set_id"]
        if timeframe_set_id not in timeframe_sets:
            timeframe_sets[timeframe_set_id] = {
                "id": row["timeframe_set_id"],
                "name": row["timeframe_set_name"],
                "timeframes": [],
            }
        if row["timeframe_id"]:
            timeframe_sets[timeframe_set_id]["timeframes"].append(
                {
                    "id": row["timeframe_id"],
                    "name": row["timeframe_name"],
                    "start": row["timeframe_start"],
                    "end": row["timeframe_end"],
                    "interval": row["timeframe_interval"],
                }
            )
    return list(timeframe_sets.values())


def get_timeframes():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM timeframe")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def get_timeframes_by_timeframe_set_id(timeframe_set_id):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        "SELECT * FROM timeframe WHERE timeframe_set_id = ?", (timeframe_set_id,)
    )
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def choose_timeframe_set():
    timeframe_sets = get_timeframe_sets()

    print("Available timeframe sets:")
    for i, config in enumerate(timeframe_sets):
        print(f"{i + 1}: {config}")

    choice = int(input("Select a timeframe set by number: ")) - 1
    set_name = timeframe_sets[choice]
    print(f"Timeframe set selected: {set_name}")
    return set_name
