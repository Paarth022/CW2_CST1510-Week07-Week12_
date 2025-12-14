from typing import Optional
import hashlib
from models.user import User
from services.database_manager import DatabaseManager

class SimpleHasher:

    @staticmethod
    def hash_password(plain: str) -> str:
        return hashlib.sha256(plain.encode("utf-8")).hexdigest()
    
    @staticmethod
    def check_password(plain: str, hashed: str) -> bool:
        return SimpleHasher.hash_password(plain) == hashed


class AuthManager:
    
    def __init__(self, db: DatabaseManager):
        self._db = db
    
    def register_user(self, username: str, password: str, role: str = "user") -> bool:
        # Check if user already exists
        existing = self._db.fetch_one(
            "SELECT username FROM users WHERE username = ?",
            (username,)
        )
        if existing:
            return False  # User already exists
        
        password_hash = SimpleHasher.hash_password(password)
        try:
            self._db.execute_query(
                "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
                (username, password_hash, role),
            )
            return True
        except Exception as e:
            print(f"Error registering user: {e}")
            return False
    
    def login_user(self, username: str, password: str) -> Optional[User]:
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )
        if row is None:
            return None
        
        username_db, password_hash_db, role_db = row
        if SimpleHasher.check_password(password, password_hash_db):
            return User(username_db, password_hash_db, role_db)
        
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        row = self._db.fetch_one(
            "SELECT username, password_hash, role FROM users WHERE username = ?",
            (username,),
        )
        if row is None:
            return None
        
        username_db, password_hash_db, role_db = row
        return User(username_db, password_hash_db, role_db)