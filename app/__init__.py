"""
Factory function to create Flask app instance with configuration.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name="development"):
    """Create and configure Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Create database tables within app context
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import main_bp, session_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(api_bp)
    
    return app
