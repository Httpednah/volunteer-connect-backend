"""
Seed data for Volunteer Connect backend
Populates Users, Organizations, Opportunities, Applications, and Payments
"""

from app import app, db
from models import User, Organization, Opportunity, Application, Payment

def seed():
    with app.app_context():
        # 1️ Clear existing data
        Payment.query.delete()
        Application.query.delete()
        Opportunity.query.delete()
        Organization.query.delete()
        User.query.delete()
        db.session.commit()
        print("Cleared existing data...")

        # 2️ Create Users
        user1 = User(name="Alice Volunteer", email="alice@vol.com", role="volunteer")
        user1.set_password("password123")

        user2 = User(name="Bob Volunteer", email="bob@vol.com", role="volunteer")
        user2.set_password("password123")

        owner1 = User(name="Carol OrgOwner", email="carol@org.com", role="organization")
        owner1.set_password("password123")

        owner2 = User(name="Dave OrgOwner", email="dave@org.com", role="organization")
        owner2.set_password("password123")

        db.session.add_all([user1, user2, owner1, owner2])
        db.session.commit()
        print("Created users...")

        # 3️ Create Organizations
        org1 = Organization(
            name="Local Food Bank",
            description="Helps feed local families",
            location="123 Main St",
            owner_id=owner1.id
        )
        org2 = Organization(
            name="City Animal Shelter",
            description="Rescues and cares for animals",
            location="456 Oak Ave",
            owner_id=owner2.id
        )
        org3 = Organization(
            name="Youth Mentoring Program",
            description="Supports youth education",
            location="789 Elm St",
            owner_id=owner1.id
        )

        db.session.add_all([org1, org2, org3])
        db.session.commit()
        print("Created organizations...")

        # 4️ Create Opportunities (assign created_by = org.owner_id)
        opp_data = [
            ("Food Sorting Helper", "Sort and package food donations", "Food Bank", 4, org1),
            ("Delivery Driver", "Deliver food packages to elderly residents", "Various", 3, org1),
            ("Dog Walker", "Walk shelter dogs", "Animal Shelter", 2, org2),
            ("Cat Caretaker", "Feed and groom cats", "Animal Shelter", 3, org2),
            ("Math Tutor", "Help students with math homework", "Community Center", 2, org3),
            ("Reading Buddy", "Improve literacy with young students", "Public Library", 1, org3),
            ("Community Garden Helper", "Maintain community garden", "Community Garden", 5, org1),
            ("Event Volunteer", "Assist at animal shelter fundraising events", "Various", 6, org2),
        ]

        opportunities = []
        for title, desc, location, duration, org in opp_data:
            opp = Opportunity(
                title=title,
                description=desc,
                location=location,
                duration=duration,
                organization_id=org.id,
                created_by=org.owner_id  # <-- assign the owner as creator
            )
            opportunities.append(opp)

        db.session.add_all(opportunities)
        db.session.commit()
        print("Created opportunities...")

        # 5️ Create Applications
        apps = [
            Application(user_id=user1.id, opportunity_id=opportunities[0].id, motivation_message="I love helping the community!"),
            Application(user_id=user1.id, opportunity_id=opportunities[2].id, motivation_message="I enjoy working with animals"),
            Application(user_id=user2.id, opportunity_id=opportunities[4].id, motivation_message="I want to help students learn math"),
            Application(user_id=user2.id, opportunity_id=opportunities[5].id, motivation_message="I enjoy reading with kids"),
            Application(user_id=user2.id, opportunity_id=opportunities[3].id, motivation_message="I am comfortable caring for cats"),
        ]

        db.session.add_all(apps)
        db.session.commit()
        print("Created applications...")

        # 6️ Create Payments
        pays = [
            Payment(user_id=user1.id, opportunity_id=opportunities[0].id, amount=50.0, payment_status="completed"),
            Payment(user_id=user2.id, opportunity_id=opportunities[4].id, amount=30.0, payment_status="pending"),
            Payment(user_id=user2.id, opportunity_id=opportunities[5].id, amount=20.0, payment_status="completed"),
        ]

        db.session.add_all(pays)
        db.session.commit()
        print("Created payments...")

        print("Seed complete!")

if __name__ == "__main__":
    seed()
