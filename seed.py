"""
Seed data for Volunteer Connect
Used for development and testing
"""

from app import app, db
from models import User, Organization, Opportunity
from werkzeug.security import generate_password_hash

def seed_opportunities():
    """Add sample users, organizations, and volunteer opportunities"""
    with app.app_context():
        # Clear existing data
        db.drop_all()
        db.create_all()

        # ----------------------------
        # 1️⃣ Create Users (organization owners)
        # ----------------------------
        owner1 = User(
            name="Alice Johnson",
            email="alice@example.com",
            role="organization",
            password_hash=generate_password_hash("password123")
        )
        owner2 = User(
            name="Bob Smith",
            email="bob@example.com",
            role="organization",
            password_hash=generate_password_hash("password123")
        )
        owner3 = User(
            name="Carol Lee",
            email="carol@example.com",
            role="organization",
            password_hash=generate_password_hash("password123")
        )

        db.session.add_all([owner1, owner2, owner3])
        db.session.commit()  # IDs generated here

        # ----------------------------
        # 2️⃣ Create Organizations with valid owner_id
        # ----------------------------
        org1 = Organization(name="Local Food Bank", owner_id=owner1.id)
        org2 = Organization(name="Animal Shelter", owner_id=owner2.id)
        org3 = Organization(name="Youth Mentoring Program", owner_id=owner3.id)

        db.session.add_all([org1, org2, org3])
        db.session.commit()  # IDs generated here

        # ----------------------------
        # 3️⃣ Create Opportunities
        # ----------------------------
        opportunities = [
            Opportunity(
                organization_id=org1.id,
                title="Food Sorting Helper",
                description="Help sort and package food donations for families in need. No experience necessary.",
                location="Downtown Food Bank, 123 Main St",
                duration=4,
                created_by=owner1.id
            ),
            Opportunity(
                organization_id=org1.id,
                title="Delivery Driver",
                description="Deliver food packages to elderly and disabled residents.",
                location="Various locations",
                duration=3,
                created_by=owner1.id
            ),
            Opportunity(
                organization_id=org2.id,
                title="Dog Walker",
                description="Walk shelter dogs to keep them healthy and happy.",
                location="City Animal Shelter, 456 Oak Ave",
                duration=2,
                created_by=owner2.id
            ),
            Opportunity(
                organization_id=org2.id,
                title="Cat Caretaker",
                description="Feed, groom, and socialize cats at the shelter.",
                location="City Animal Shelter, 456 Oak Ave",
                duration=3,
                created_by=owner2.id
            ),
            Opportunity(
                organization_id=org3.id,
                title="Math Tutor",
                description="Help students with math homework. Make a difference!",
                location="Community Center, 789 Elm St",
                duration=2,
                created_by=owner3.id
            ),
            Opportunity(
                organization_id=org3.id,
                title="Reading Buddy",
                description="Read with young students to improve literacy.",
                location="Public Library, 321 Book Lane",
                duration=1,
                created_by=owner3.id
            ),
        ]

        db.session.add_all(opportunities)
        db.session.commit()

        print(f"Seeded {len(opportunities)} opportunities across 3 organizations")


if __name__ == "__main__":
    seed_opportunities()
