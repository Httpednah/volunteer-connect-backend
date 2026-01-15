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

 # ---------- OPPORTUNITY ----------
    opportunity = Opportunity(
        title="Beach Cleanup",
        description="Help clean the beach",
        location="Mombasa",
        duration=5,
        organization_id=org.id
    )

    db.session.add(opportunity)
    db.session.commit()

    # ---------- APPLICATION ----------
    application = Application(
        user_id=volunteer.id,
        opportunity_id=opportunity.id,
        motivation_message="I love helping the community",
        status="pending"
    )

    db.session.add(application)
    db.session.commit()

   # ---------- PAYMENT ----------
    payment = Payment(
        user_id=volunteer.id,
        opportunity_id=opportunity.id,
        amount=1000,
        payment_status="completed",
        payment_date=datetime.utcnow()
    )

    db.session.add(payment)
    db.session.commit()

    print("✅ Seed complete")
    
