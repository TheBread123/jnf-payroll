from flask import Blueprint
from .controllers.user_controller import UserController

# Create blueprint for API routes
api_bp = Blueprint("api", __name__, url_prefix="/api")

# Initialize controller
user_controller = UserController()


# User authentication routes
@api_bp.route("/login", methods=["POST"])
def login():
    """User login endpoint"""
    response_data, status_code = user_controller.login()
    return response_data, status_code


@api_bp.route("/verify-token", methods=["POST"])
def verify_token():
    """Token verification endpoint"""
    response_data, status_code = user_controller.verify_token()
    return response_data, status_code


@api_bp.route("/protected", methods=["GET"])
def protected():
    """Protected endpoint requiring authentication"""
    response_data, status_code = user_controller.get_protected_data()
    return response_data, status_code


@api_bp.route("/users", methods=["POST"])
def create_user():
    """Create new user endpoint"""
    response_data, status_code = user_controller.create_user()
    return response_data, status_code


# Health check route
@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    from .views.user_view import UserView

    view = UserView()
    return view.health_check_response()
