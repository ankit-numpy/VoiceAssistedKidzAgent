"""
Configuration settings for different environments.
"""
import os
from datetime import timedelta

class Config:
    """Base configuration."""
    FLASK_ENV = "development"
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///kidzagent.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_REFRESH_EACH_REQUEST = True
    
    # Azure/LLM Configuration
    AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT", "")
    AZURE_API_KEY = os.getenv("AZURE_API_KEY", "")
    AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4")
    
    # Google Cloud Speech-to-Text (optional)
    GOOGLE_CLOUD_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
    
    # Child Safety
    MAX_SESSION_DURATION = 30  # minutes
    MIN_AGE = 5
    MAX_AGE = 8
    
    # Feature Flags
    ENABLE_SPEECH_RECOGNITION = True
    ENABLE_FEEDBACK = True
    ENABLE_PROGRESS_TRACKING = True
    ENABLE_PARENTAL_DASHBOARD = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv("SECRET_KEY", "CHANGE_THIS_IN_PRODUCTION")

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
