from flask import request, current_app
from ..models.user import UserRepository
from ..views.user_view import UserView
from typing import Tuple, Dict, Any


class UserController:
    """Controller for handling user-related requests"""

    def __init__(self):
        self.user_repository = UserRepository()
        self.user_view = UserView()

    def login(self) -> Tuple[Dict[str, Any], int]:
        """Handle user login request"""
        try:
            # Get request data
            data = request.get_json()

            if not data:
                return self.user_view.error_response("No data provided"), 400

            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return (
                    self.user_view.error_response("Username and password are required"),
                    400,
                )

            # Authenticate user
            user = self.user_repository.authenticate(username, password)

            if not user:
                return self.user_view.error_response("Invalid credentials"), 401

            # Generate token
            token = user.generate_token(current_app.config["SECRET_KEY"])

            return self.user_view.login_success_response(user, token), 200

        except Exception as e:
            return self.user_view.error_response(f"Login failed: {str(e)}"), 500

    def verify_token(self) -> Tuple[Dict[str, Any], int]:
        """Handle token verification request"""
        try:
            data = request.get_json()
            token = data.get("token") if data else None

            if not token:
                return self.user_view.error_response("Token required"), 400

            # Verify token
            from ..models.user import User

            user_data = User.verify_token(token, current_app.config["SECRET_KEY"])

            if not user_data:
                return self.user_view.error_response("Invalid or expired token"), 401

            return self.user_view.token_verification_response(user_data), 200

        except Exception as e:
            return (
                self.user_view.error_response(f"Token verification failed: {str(e)}"),
                500,
            )

    def get_protected_data(self) -> Tuple[Dict[str, Any], int]:
        """Handle protected endpoint request"""
        try:
            # Extract token from Authorization header
            auth_header = request.headers.get("Authorization")

            if not auth_header:
                return self.user_view.error_response("Token required"), 401

            # Remove 'Bearer ' prefix if present
            token = (
                auth_header[7:] if auth_header.startswith("Bearer ") else auth_header
            )

            # Verify token
            from ..models.user import User

            user_data = User.verify_token(token, current_app.config["SECRET_KEY"])

            if not user_data:
                return self.user_view.error_response("Invalid or expired token"), 401

            return self.user_view.protected_data_response(user_data), 200

        except Exception as e:
            return (
                self.user_view.error_response(
                    f"Failed to access protected data: {str(e)}"
                ),
                500,
            )

    def create_user(self) -> Tuple[Dict[str, Any], int]:
        """Handle user creation request"""
        try:
            data = request.get_json()

            if not data:
                return self.user_view.error_response("No data provided"), 400

            username = data.get("username")
            password = data.get("password")
            email = data.get("email")
            role = data.get("role", "user")

            if not all([username, password, email]):
                return (
                    self.user_view.error_response(
                        "Username, password, and email are required"
                    ),
                    400,
                )

            # Create user
            user = self.user_repository.create_user(username, password, email, role)

            return self.user_view.user_created_response(user), 201

        except ValueError as e:
            return self.user_view.error_response(str(e)), 400
        except Exception as e:
            return self.user_view.error_response(f"User creation failed: {str(e)}"), 500
