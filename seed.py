"""
Seed data for Volunteer Connect backend
Populates Users, Organizations, Opportunities, Applications, and Payments
"""

from app import app, db
from models import User, Organization, Opportunity, Application, Payment

def seed():
    with app.app_context():
        # 1️Clear existing data
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
        org1 = Organization(name="Local Food Bank", description="Helps feed local families", location="123 Main St", owner_id=owner1.id)
        org2 = Organization(name="City Animal Shelter", description="Rescues and cares for animals", location="456 Oak Ave", owner_id=owner2.id)
        org3 = Organization(name="Youth Mentoring Program", description="Supports youth education", location="789 Elm St", owner_id=owner1.id)

        db.session.add_all([org1, org2, org3])
        db.session.commit()
        print("Created organizations...")

        # 4️Create Opportunities
        opp1 = Opportunity(title="Food Sorting Helper", description="Sort and package food donations", location="Food Bank", duration=4, organization_id=org1.id)
        opp2 = Opportunity(title="Delivery Driver", description="Deliver food packages to elderly residents", location="Various", duration=3, organization_id=org1.id)
        opp3 = Opportunity(title="Dog Walker", description="Walk shelter dogs", location="Animal Shelter", duration=2, organization_id=org2.id)
        opp4 = Opportunity(title="Cat Caretaker", description="Feed and groom cats", location="Animal Shelter", duration=3, organization_id=org2.id)
        opp5 = Opportunity(title="Math Tutor", description="Help students with math homework", location="Community Center", duration=2, organization_id=org3.id)
        opp6 = Opportunity(title="Reading Buddy", description="Improve literacy with young students", location="Public Library", duration=1, organization_id=org3.id)
        opp7 = Opportunity(title="Community Garden Helper", description="Maintain community garden", location="Community Garden", duration=5, organization_id=org1.id)
        opp8 = Opportunity(title="Event Volunteer", description="Assist at animal shelter fundraising events", location="Various", duration=6, organization_id=org2.id)

        db.session.add_all([opp1, opp2, opp3, opp4, opp5, opp6, opp7, opp8])
        db.session.commit()
        print("Created opportunities...")

        # 5️Create Applications (many-to-many user-submitted attribute)
        app1 = Application(user_id=user1.id, opportunity_id=opp1.id, motivation_message="I love helping the community!")
        app2 = Application(user_id=user1.id, opportunity_id=opp3.id, motivation_message="I enjoy working with animals")
        app3 = Application(user_id=user2.id, opportunity_id=opp5.id, motivation_message="I want to help students learn math")
        app4 = Application(user_id=user2.id, opportunity_id=opp6.id, motivation_message="I enjoy reading with kids")
        app5 = Application(user_id=user2.id, opportunity_id=opp4.id, motivation_message="I am comfortable caring for cats")

        db.session.add_all([app1, app2, app3, app4, app5])
        db.session.commit()
        print("Created applications...")

        # 6️Create Payments
        pay1 = Payment(user_id=user1.id, opportunity_id=opp1.id, amount=50.0, payment_status="completed")
        pay2 = Payment(user_id=user2.id, opportunity_id=opp5.id, amount=30.0, payment_status="pending")
        pay3 = Payment(user_id=user2.id, opportunity_id=opp6.id, amount=20.0, payment_status="completed")

        db.session.add_all([pay1, pay2, pay3])
        db.session.commit()
        print("Created payments...")

        print("Seed complete!")

if __name__ == "__main__":
    seed()
