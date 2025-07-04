from typing import Dict, Any
import datetime


class UserView:
    """View class for formatting user-related responses"""

    def error_response(self, message: str) -> Dict[str, Any]:
        """Format error response"""
        return {"error": message, "timestamp": datetime.datetime.utcnow().isoformat()}

    def login_success_response(self, user, token: str) -> Dict[str, Any]:
        """Format successful login response"""
        return {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": user.to_dict(),
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

    def token_verification_response(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format token verification response"""
        return {
            "valid": True,
            "user": user_data,
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

    def protected_data_response(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format protected data response"""
        return {
            "message": f'Welcome {user_data["username"]}! This is a protected route.',
            "user": user_data,
            "backend_status": "Connected successfully!",
            "deployment_info": {
                "environment": "Development",
                "python_version": "3.x",
                "framework": "Flask",
                "frontend": "React",
                "architecture": "MVC",
            },
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

    def user_created_response(self, user) -> Dict[str, Any]:
        """Format user creation response"""
        return {
            "success": True,
            "message": "User created successfully",
            "user": user.to_dict(),
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }

    def health_check_response(self) -> Dict[str, Any]:
        """Format health check response"""
        return {
            "status": "healthy",
            "message": "JNF Payroll API is running",
            "architecture": "MVC",
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
