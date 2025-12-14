import sqlite3

def create_users_table(conn):
    """Create users table"""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'user',
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("✅ Users table created")

def create_cyber_incidents_table(conn):
    """Create cyber incidents table"""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cyber_incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        incident_type TEXT,
        severity TEXT,
        status TEXT,
        source_ip TEXT,
        target_ip TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("✅ Cyber incidents table created")

def create_it_tickets_table(conn):
    """Create IT tickets table"""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS it_tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        status TEXT,
        priority TEXT,
        category TEXT,
        assigned_to TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("✅ IT tickets table created")

def create_datasets_metadata_table(conn):
    """Create datasets metadata table"""
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS datasets_metadata (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        category TEXT,
        owner TEXT,
        format TEXT,
        file_path TEXT,
        created_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    print("✅ Datasets metadata table created")

def create_all_tables(conn):
    """Create all tables"""
    create_users_table(conn)
    create_cyber_incidents_table(conn)
    create_it_tickets_table(conn)
    create_datasets_metadata_table(conn)
    print("\n✅ All tables created successfully!")

if __name__ == "__main__":
    import sqlite3
    conn = sqlite3.connect("intelligence_platform.db")
    create_all_tables(conn)
    conn.close()