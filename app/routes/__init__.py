"""
Routes module initialization.
Defines all blueprints for the Flask application.
"""
from flask import Blueprint

# Create blueprints
main_bp = Blueprint("main", __name__)
session_bp = Blueprint("session", __name__, url_prefix="/session")
api_bp = Blueprint("api", __name__, url_prefix="/api")

# Import route handlers to register them
from app.routes import main, session, api
