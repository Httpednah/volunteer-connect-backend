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

# ---------- USERS ----------
    volunteer = User(
        name="Craig Volunteer",
        email="volunteer@test.com",
        password=generate_password_hash("password123"),
        role="volunteer"
    )

    org_owner = User(
        name="Org Owner",
        email="org@test.com",
        password=generate_password_hash("password123"),
        role="organization"
    )

    db.session.add_all([volunteer, org_owner])
    db.session.commit()

  # ---------- ORGANIZATION ----------
    org = Organization(
        name="Helping Hands",
        description="Community volunteer organization",
        location="Nairobi",
        owner_id=org_owner.id
    )

    db.session.add(org)
    db.session.commit()
