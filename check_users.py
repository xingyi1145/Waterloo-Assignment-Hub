import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from src.backend.database import SessionLocal
from src.backend.models import User
from src.backend.auth import verify_password

def check_users():
    db = SessionLocal()
    users = db.query(User).all()
    
    print(f"Found {len(users)} users in database:")
    print("-" * 50)
    
    for user in users:
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Identity: {user.identity}")
        
        # Test password
        is_valid = verify_password("password123", user.password_hash)
        print(f"Password 'password123' valid? {is_valid}")
        print("-" * 50)
    
    db.close()

if __name__ == "__main__":
    check_users()
