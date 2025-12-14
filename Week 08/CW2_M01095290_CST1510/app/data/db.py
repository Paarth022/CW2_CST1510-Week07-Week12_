"""Database Connection and Setup Module"""

import sqlite3
from pathlib import Path

# Define the database path
DB_PATH = Path("DATA") / "intelligence_platform.db"


def connect_database(db_path=DB_PATH):
    """Connect to SQLite database. Creates file if it doesn't exist."""
    # Ensure the DATA directory exists
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(str(db_path))


def close_database(conn):
    """Close the database connection safely."""
    if conn:
        conn.close()


def setup_database():
    """
    Initializes the database structure by creating all necessary tables
    for the IT ticketing system and populating lookup tables.
    """
    conn = connect_database()
    cursor = conn.cursor()

    # --- 1. CREATE USERS TABLE ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            role TEXT NOT NULL DEFAULT 'user' -- e.g., 'user', 'agent', 'admin'
        );
    """)

    # --- 2. CREATE STATUSES TABLE ---
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS statuses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status_name TEXT UNIQUE NOT NULL
        );
    """)

    # Populate statuses table only if it's empty
    # We check if 'Open' exists, and if not, we insert the initial statuses.
    cursor.execute("SELECT COUNT(*) FROM statuses WHERE status_name = 'Open'")
    if cursor.fetchone()[0] == 0:
        initial_statuses = [
            ('Open',), 
            ('In Progress',), 
            ('Awaiting User Reply',), 
            ('Closed',)
        ]
        cursor.executemany(
            "INSERT INTO statuses (status_name) VALUES (?)",
            initial_statuses
        )

    #  3. Create table fot IT TICKETS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL, -- e.g., 'Low', 'Medium', 'High', 'Critical'
            
            -- Foreign Keys
            status_id INTEGER NOT NULL, 
            reported_by_user_id INTEGER NOT NULL,
            assigned_agent_id INTEGER, -- NULLable if unassigned
            
            -- Timestamps (Use DATETIME for explicit storage)
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,

            -- Constraints
            FOREIGN KEY (status_id) REFERENCES statuses(id),
            FOREIGN KEY (reported_by_user_id) REFERENCES users(id),
            FOREIGN KEY (assigned_agent_id) REFERENCES users(id)
        );
    """)

    # 4.CREATE TICKET_UPDATES TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ticket_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL, -- The user/agent who left the comment
            comment TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

            -- Constraints
            FOREIGN KEY (ticket_id) REFERENCES it_tickets(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    """)
    
    conn.commit()
    conn.close()


def reset_database():
    """Drops all tables to allow for clean re-creation during testing/development."""
    conn = connect_database()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS ticket_updates")
    cursor.execute("DROP TABLE IF EXISTS it_tickets")
    cursor.execute("DROP TABLE IF EXISTS statuses")
    cursor.execute("DROP TABLE IF EXISTS users")
    conn.commit()
    conn.close()
    print(f"Database tables reset successfully in {DB_PATH}.")


if __name__ == "__main__":
    try:
        setup_database()
        conn = connect_database()
        print(f" Connected to database: {DB_PATH}")
        print(" Database schema initialized/verified.")
        close_database(conn)
    except Exception as e:
        print(f" Error: {e}")
        