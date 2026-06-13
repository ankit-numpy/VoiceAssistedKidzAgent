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
    
    # Register blueprints
    from app.routes import main_bp, session_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(session_bp)
    app.register_blueprint(api_bp)
    
    # Create database tables within app context (after blueprints)
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Warning: Could not create database tables: {e}")
    
    # Error handlers
    @app.errorhandler(500)
    def internal_error(e):
        print(f"Internal Server Error: {e}")
        return {"error": "Internal Server Error", "message": str(e)}, 500
    
    @app.errorhandler(404)
    def not_found(e):
        return {"error": "Not Found"}, 404
    
    # Health check endpoint
    @app.route('/health')
    def health():
        return {"status": "ok", "app": "Voice Assisted KidzAgent"}, 200
    
    return app
