from flask import Flask, send_from_directory, render_template, jsonify
from flask_cors import CORS
import datetime
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# Enable CORS for all routes with specific configuration
CORS(
    app,
    origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
    ],
    methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
)


# Secret key for JWT tokens
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY", "dev-secret-key-change-in-production"
)

# Import and register blueprints
from backend.routes import api_bp

app.register_blueprint(api_bp)


@app.route("/")
def serve_react_app():
    """Serve the React app for the root route"""
    try:
        return render_template("index.html")
    except Exception:
        # Fallback if templates are not available (development mode)
        return jsonify(
            {
                "status": "healthy",
                "message": "JNF Payroll API is running - Frontend not built yet",
                "timestamp": datetime.datetime.utcnow().isoformat(),
            }
        )


@app.route("/<path:path>")
def serve_react_routes(path):
    """Serve React app for all frontend routes"""
    try:
        # Try to serve static files first
        if os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        # Otherwise serve the main React app
        return render_template("index.html")
    except Exception:
        return jsonify({"error": "Resource not found"}), 404


@app.route("/health")
def health_check():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "message": "JNF Payroll API is running",
            "architecture": "MVC",
            "timestamp": datetime.datetime.utcnow().isoformat(),
        }
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
