import bcrypt
import os


USER_FILE = "users.txt"

def hash_password(plain_text_password):
    """
    Hashes the plain text password using bcrypt.
    """
    password_bytes = plain_text_password.encode('utf-8')
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
   
    return hashed.decode('utf-8')

def verify_password(plain_text_password, hashed_password):
    """
    Verifies a plain text password against a stored bcrypt hash.
    """
    try:
        password_bytes = plain_text_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')
      
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False



def _load_users():
    """
    Loads all users from USER_FILE into a dictionary.
    Format in file: username,password_hash,role
    Returns: {username: {'password_hash': hash, 'role': role}, ...}
    """
    users = {}
    if not os.path.exists(USER_FILE):
        return users 
    with open(USER_FILE, 'r') as f:
        for line in f:
            try:
                
                username, password_hash, role = line.strip().split(',', 2)
                users[username] = {'password_hash': password_hash, 'role': role}
            except ValueError:
                
                continue
    return users

def _save_users(users):
    """
    Writes the entire users dictionary back to the USER_FILE.
    """
    with open(USER_FILE, 'w') as f:
        for username, data in users.items():
            
            line = f"{username},{data['password_hash']},{data['role']}\n"
            f.write(line)



def login_user(username, password):
    """
    Checks if a user exists and if the provided password is correct.
    """
    try:
        users = _load_users()
        user_data = users.get(username)
        
        if not user_data:
            return False, "Username not found."
        
        
        if verify_password(password, user_data['password_hash']):
            return True, user_data['role']
        else:
            return False, "Invalid password."
    
    except Exception as e:
        
        return False, f"Login error: {str(e)}"

def register_user(username, password, role="user"):
    """
    Registers a new user and stores the credentials in the file.
    """
    try:
        users = _load_users()
        
        if username in users:
            return False, f"Username '{username}' already exists."
        
        hashed = hash_password(password)
        
     
        users[username] = {
            'password_hash': hashed, 
            'role': role
        }
        
      
        _save_users(users)
        
        return True, f"User '{username}' registered successfully!"
    
    except Exception as e:
        return False, f"Registration error: {str(e)}"

def user_exists(username):
    """
    Checks if a username is present in the file.
    """
    try:
        users = _load_users()
        return username in users
    except Exception:
     
        return False
if __name__ == '__main__':
    # 1. Register a new user
    success, message = register_user("testuser", "securepassword123", "admin")
    print(f"Registration: {success}, {message}")

    # 2. Check if the user exists
    exists = user_exists("testuser")
    print(f"User exists: {exists}")
    
    # 3. Log in with correct credentials
    logged_in, result = login_user("testuser", "securepassword123")
    print(f"Login success: {logged_in}, Role/Message: {result}")

    # 4. Try to log in with incorrect password
    logged_in_fail, result_fail = login_user("testuser", "wrongpassword")
    print(f"Login failure: {logged_in_fail}, Message: {result_fail}")