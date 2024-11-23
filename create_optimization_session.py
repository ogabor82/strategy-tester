import db.db

def get_user_inputs():
    session_name = input("Enter the optimization session name: ")
    session_details = input("Enter the optimization session details: ")
    return session_name, session_details

def save_session(session_name, session_details):
    cursor = db.db.DB.cursor()
    cursor.execute("INSERT INTO optimization_session (name, details) VALUES (?, ?)", (session_name, session_details))
    db.db.DB.commit()

def create_optimization_session():
    session_name, session_details = get_user_inputs()
    print(f"Creating optimization session with name: {session_name}")
    print(f"Details: {session_details}")

    save_session(session_name, session_details)

    print("Optimization session created successfully.")