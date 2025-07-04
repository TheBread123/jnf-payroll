from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from typing import Optional, Dict, Any


class User:
    """User model for handling user data and authentication logic"""

    def __init__(self, username: str, password: str, email: str, role: str = "user"):
        self.username = username
        self.password = password
        self.email = email
        self.role = role

    def to_dict(self) -> Dict[str, Any]:
        """Convert user object to dictionary (excluding password)"""
        return {"username": self.username, "email": self.email, "role": self.role}

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password for storing in the database"""
        return generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify a password against the stored hash"""
        return check_password_hash(self.password, password)

    def generate_token(self, secret_key: str, expiration_hours: int = 24) -> str:
        """Generate a JWT token for the user"""
        payload = {
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "exp": datetime.datetime.utcnow()
            + datetime.timedelta(hours=expiration_hours),
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")

    @staticmethod
    def verify_token(token: str, secret_key: str) -> Optional[Dict[str, Any]]:
        """Verify a JWT token and return user data if valid"""
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return {
                "username": payload["username"],
                "email": payload["email"],
                "role": payload["role"],
            }
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


class UserRepository:
    """Repository class for user data management"""

    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would connect to a database
        self.users = {
            "admin": User(
                username="admin",
                password=User.hash_password("password123"),
                email="admin@jnfpayroll.com",
                role="admin",
            ),
            "demo": User(
                username="demo",
                password=User.hash_password("demo123"),
                email="demo@jnfpayroll.com",
                role="user",
            ),
        }

    def find_by_username(self, username: str) -> Optional[User]:
        """Find a user by username"""
        return self.users.get(username)

    def create_user(
        self, username: str, password: str, email: str, role: str = "user"
    ) -> User:
        """Create a new user"""
        if username in self.users:
            raise ValueError("User already exists")

        user = User(username, User.hash_password(password), email, role)
        self.users[username] = user
        return user

    def authenticate(self, username: str, password: str) -> Optional[User]:
        """Authenticate a user with username and password"""
        user = self.find_by_username(username)
        if user and user.verify_password(password):
            return user
        return None

    def get_all_users(self) -> Dict[str, User]:
        """Get all users (for admin purposes)"""
        return self.users
