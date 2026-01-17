from app import app, db
from models import Organization, Opportunity, User, Application, Payment

def seed():
    with app.app_context():
        # Clear existing data
        Payment.query.delete()
        Application.query.delete()
        Opportunity.query.delete()
        Organization.query.delete()
        User.query.delete()
        db.session.commit()

        # ----- CREATE USERS -----
        users_data = [
            {"name": "Alice", "email": "alice@example.com", "password": "password", "role": "volunteer"},
            {"name": "Bob", "email": "bob@example.com", "password": "password", "role": "organization"}
        ]

        users = []
        for u in users_data:
            user = User(
                name=u["name"],
                email=u["email"],
                role=u["role"]
            )
            user.set_password(u["password"])
            db.session.add(user)
            users.append(user)

        db.session.commit()

        # ----- CREATE ORGANIZATIONS -----
        orgs_data = [
            {"name": "Helping Hands", "description": "Community outreach", "location": "Nairobi", "owner": users[1]},
        ]

        orgs = []
        for o in orgs_data:
            org = Organization(
                name=o["name"],
                description=o["description"],
                location=o["location"],
                owner=o["owner"]
            )
            db.session.add(org)
            orgs.append(org)

        db.session.commit()

        # ----- CREATE OPPORTUNITIES -----
        opps_data = [
            {"title": "Tree Planting", "description": "Plant trees in local park", "location": "City Park", "duration": 2, "organization": orgs[0]},
            {"title": "Beach Cleanup", "description": "Clean the beach", "location": "Mombasa Beach", "duration": 3, "organization": orgs[0]},
        ]

        for o in opps_data:
            opp = Opportunity(
                title=o["title"],
                description=o["description"],
                location=o["location"],
                duration=o["duration"],
                organization=o["organization"]
            )
            db.session.add(opp)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed()
