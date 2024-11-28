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

def get_user_inputs():
    session_name = input("Enter the backtest session name: ")
    session_details = input("Enter the backtest session details: ")
    return session_name, session_details

def save_session(session_name, session_details):
    init_db()
    cursor = DB.cursor()
    cursor.execute("INSERT INTO backtest_session (name, details) VALUES (?, ?)", (session_name, session_details))
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