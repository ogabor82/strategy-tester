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


def get_user_inputs():
    session_name = input("Enter the optimization session name: ")
    session_details = input("Enter the optimization session details: ")
    return session_name, session_details


def save_optimization_session(session_name, session_details, project_id):
    init_db()
    cursor = DB.cursor()
    cursor.execute(
        "INSERT INTO optimization_session (name, details, project_id) VALUES (?, ?, ?)",
        (session_name, session_details, project_id),
    )
    DB.commit()
    # Fetch the newly added record
    cursor.execute(
        "SELECT * FROM optimization_session WHERE id = ?", (cursor.lastrowid,)
    )
    new_record = cursor.fetchone()

    return new_record  # Return the newly added record


def create_optimization_session():
    session_name, session_details = get_user_inputs()
    print(f"Creating optimization session with name: {session_name}")
    print(f"Details: {session_details}")

    save_optimization_session(session_name, session_details)

    print("Optimization session created successfully.")


def delete_optimization_session(id):
    init_db()
    cursor = DB.cursor()
    cursor.execute("DELETE FROM optimization_session WHERE id = ?", (id,))
    cursor.execute(
        "DELETE FROM optimization_slice WHERE optimization_session_id = ?", (id,)
    )
    DB.commit()
