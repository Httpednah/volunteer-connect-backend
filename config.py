# config.py
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Base configuration for Flask app"""

    # SQLite database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'volunteer.db')
    
    # Turn off tracking modifications (optional but recommended)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key for session/cookies (required if you add authentication)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key'

