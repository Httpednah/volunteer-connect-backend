"""
Seed data for Volunteer Connect
Used for development and testing
"""

from app import app
from models import (
    db,
    User,
    Organization,
    Opportunity,
    Application,
    Payment
)
from werkzeug.security import generate_password_hash
from datetime import datetime

with app.app_context():
    print("🌱 Seeding database...")

    db.drop_all()
    db.create_all()

