from app import db, app
from models import User, Organization

with app.app_context():
    # Drop all tables and recreate them (optional: fresh start)
    db.drop_all()
    db.create_all()

    # Create users 
    user1 = User(name="Nus")
    user2 = User(name="Ednah")
    user3 = User(name="Xervi")

    db.session.add_all([user1, user2, user3])
    db.session.commit()

    #Create organizations 
    org1 = Organization(
        name="Helping Hands",
        description="Volunteers helping communities",
        location="Nairobi",
        owner_id=user1.id
    )

    org2 = Organization(
        name="Green Earth",
        description="Environmental conservation group",
        location="Mombasa",
        owner_id=user2.id
    )

    org3 = Organization(
        name="Food for All",
        description="Providing meals to the needy",
        location="Kisumu",
        owner_id=user3.id
    )

    db.session.add_all([org1, org2, org3])
    db.session.commit()

    print("Database seeded successfully!")
