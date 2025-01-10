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


def get_projects():
    init_db()
    cursor = DB.cursor()
    cursor.execute("SELECT * FROM project")
    rows = cursor.fetchall()
    return [dict(row) for row in rows]


def create_project(name, goal, details):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        "INSERT INTO project (name, goal, details) VALUES (?, ?, ?)",
        (name, goal, details),
    )
    DB.commit()
    cursor.execute("SELECT * FROM project WHERE id = ?", (cursor.lastrowid,))
    new_record = cursor.fetchone()
    return new_record


def delete_project(id):
    init_db()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM project WHERE id = ?", (id,))
    DB.commit()
