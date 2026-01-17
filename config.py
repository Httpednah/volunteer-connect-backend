# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration for Flask app"""

    # Use PostgreSQL for production (Render), SQLite for local development
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Production (Render uses postgres:// but SQLAlchemy needs postgresql://)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    else:
        # Local development
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'volunteer.db')
    
    # Turn off tracking modifications (optional but recommended)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session/cookies (required if you add authentication)
    # Generate a secure random key for production if not set
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

