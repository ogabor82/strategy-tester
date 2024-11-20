import db.db

def get_user_inputs():
    session_name = input("Enter the backtest session name: ")
    session_details = input("Enter the backtest session details: ")
    return session_name, session_details

def save_session(session_name, session_details):
    cursor = db.db.DB.cursor()
    cursor.execute("INSERT INTO backtest_session (name, details) VALUES (?, ?)", (session_name, session_details))
    db.db.DB.commit()
    

def create_session():
    session_name, session_details = get_user_inputs()
    print(f"Creating backtest session with name: {session_name}")
    print(f"Details: {session_details}")

    save_session(session_name, session_details)

    print("Backtest session created successfully.")