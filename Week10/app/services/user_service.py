import sqlite3
import bcrypt
from datetime import datetime

DATABASE_FILE = "intelligence_platform.db"

def hash_password(password: str) -> bytes:
    """Hash password using bcrypt and return as bytes"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password: str, password_hash: bytes) -> bool:
    """Verify password against hashed password"""
    try:
        # Ensure password_hash is bytes
        if isinstance(password_hash, str):
            password_hash = password_hash.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), password_hash)
    except:
        return False

def login_user(username: str, password: str) -> tuple:
    """
    Authenticate user login
    Returns: (success: bool, role: str or error_message: str)
    """
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result is None:
            return False, "❌ User not found"
        
        password_hash, role = result
        
        # Verify password
        if verify_password(password, password_hash):
            return True, role
        else:
            return False, "❌ Incorrect password"
    
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def register_user(username: str, password: str, role: str) -> tuple:
    """
    Register a new user
    Returns: (success: bool, message: str)
    """
    try:
        # Validate inputs
        if len(username) < 3 or len(username) > 20:
            return False, "❌ Username must be 3-20 characters"
        
        if len(password) < 6:
            return False, "❌ Password must be at least 6 characters"
        
        # Hash password with bcrypt
        password_hash = hash_password(password)
        
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, created_date)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, role, datetime.now()))
            conn.commit()
            conn.close()
            
            return True, f"✅ User '{username}' registered successfully!"
        
        except sqlite3.IntegrityError:
            conn.close()
            return False, "❌ Username already exists"
    
    except Exception as e:
        return False, f"❌ Error: {str(e)}"

def user_exists(username: str) -> bool:
    """Check if user exists"""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None
    except:
        return False