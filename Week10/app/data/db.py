import sqlite3

DATABASE_FILE = "intelligence_platform.db"

def connect_database():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def close_database(conn):
    if conn:
        conn.close()

def initialize_database():
    conn = connect_database()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)
    
    conn.commit()
    close_database(conn)