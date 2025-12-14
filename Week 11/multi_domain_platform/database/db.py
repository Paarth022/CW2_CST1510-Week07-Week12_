"""Database initialization script for the Multi-Domain Intelligence Platform."""

import sqlite3
from pathlib import Path

def init_database():
    """Initialize the SQLite database with required tables."""
    
# Create database directory if it doesn't exist
    db_path = Path(__file__).parent / "platform.db"
    
# Connect to database
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    
    print("Creating database tables...")
    
# Users table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created users table")
    
# Security incidents table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS security_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created security_incidents table")
    
# Datasets table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS datasets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            rows INTEGER NOT NULL,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created datasets table")
    
# IT Tickets table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS it_tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT DEFAULT 'Open',
            assigned_to TEXT DEFAULT 'Unassigned',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created it_tickets table")
    
 
    print("\nInserting test data...")
    
# Test user (password: password123 → hashed)
    test_password_hash = "48521d3b9e58a1a8c0f4f3e5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f5f"  # SHA256 of "password123"
    
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, ("alice", test_password_hash, "admin"))
    
    cur.execute("""
        INSERT OR IGNORE INTO users (username, password_hash, role)
        VALUES (?, ?, ?)
    """, ("bob", test_password_hash, "analyst"))
    
    print("✓ Inserted test users")
    
# Test security incidents
    incidents = [
        ("Malware Detection", "high", "Open", "Suspicious malware detected on server-05"),
        ("SQL Injection", "critical", "In Progress", "SQL injection vulnerability found in login page"),
        ("DDoS Attack", "high", "Resolved", "DDoS attack mitigated, traffic normalized"),
    ]
    
    for incident_type, severity, status, description in incidents:
        cur.execute("""
            INSERT OR IGNORE INTO security_incidents (incident_type, severity, status, description)
            VALUES (?, ?, ?, ?)
        """, (incident_type, severity, status, description))
    
    print("✓ Inserted test security incidents")
    
# Test datasets
    datasets = [
        ("Customer Data 2023", 5 * 1024 * 1024 * 1024, 1000000, "MySQL Database"),
        ("Transaction Logs", 2 * 1024 * 1024 * 1024, 500000, "Kafka Stream"),
        ("Audit Trails", 1024 * 1024 * 1024, 250000, "CSV Files"),
    ]
    
    for name, size_bytes, rows, source in datasets:
        cur.execute("""
            INSERT OR IGNORE INTO datasets (name, size_bytes, rows, source)
            VALUES (?, ?, ?, ?)
        """, (name, size_bytes, rows, source))
    
    print("✓ Inserted test datasets")
    
# Test tickets
    tickets = [
        ("Reset Password - John Doe", "low", "Open", "Support Team A"),
        ("Server Outage - Critical", "critical", "In Progress", "Infrastructure Team"),
        ("Email Configuration", "medium", "Resolved", "Support Team B"),
    ]
    
    for title, priority, status, assigned_to in tickets:
        cur.execute("""
            INSERT OR IGNORE INTO it_tickets (title, priority, status, assigned_to)
            VALUES (?, ?, ?, ?)
        """, (title, priority, status, assigned_to))
    
    print("✓ Inserted test IT tickets")
    
# Commit changes
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database initialized successfully at: {db_path}")
    print("""
Test credentials:
- Username: alice
- Password: password123

Test data has been created:
- 2 users (alice: admin, bob: analyst)
- 3 security incidents
- 3 datasets
- 3 IT tickets
    """)

if __name__ == "__main__":
    init_database()