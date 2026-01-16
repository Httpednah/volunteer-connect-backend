"""
Seed data for Volunteer Connect database
"""

from app import app
from extensions import db
from models import User, Organization, Opportunity

def seed_opportunities():
    """Add sample volunteer opportunities to the database."""
    with app.app_context():
        # Reset the database: Drop all existing tables and re-create them
        print("Resetting database...")
        db.drop_all()
        db.create_all()
        
        # Create a default administrator/organization user to own the sample records
        print("Creating sample user...")
        user = User(name="Admin User", email="admin@example.com", role="organization")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
        # Create sample organizations linked to the admin user
        print("Creating sample organizations...")
        org1 = Organization(name='Local Food Bank', owner_id=user.id)
        org2 = Organization(name='Animal Shelter', owner_id=user.id)
        org3 = Organization(name='Youth Mentoring Program', owner_id=user.id)
        
        db.session.add_all([org1, org2, org3])
        db.session.commit()
        
        # Create a diverse set of volunteer opportunities across the organizations
        print("Creating sample opportunities...")
        opportunities = [
            Opportunity(
                organization_id=org1.id,
                title='Food Sorting Helper',
                description='Help sort and package food donations for families in need.',
                location='Downtown Food Bank, 123 Main St',
                duration=4
            ),
            Opportunity(
                organization_id=org1.id,
                title='Delivery Driver',
                description='Deliver food packages to elderly and disabled residents.',
                location='Various locations',
                duration=3
            ),
            Opportunity(
                organization_id=org2.id,
                title='Dog Walker',
                description='Walk shelter dogs to keep them healthy and happy.',
                location='City Animal Shelter, 456 Oak Ave',
                duration=2
            ),
            Opportunity(
                organization_id=org2.id,
                title='Cat Caretaker',
                description='Feed, groom, and socialize cats at the shelter.',
                location='City Animal Shelter, 456 Oak Ave',
                duration=3
            ),
            Opportunity(
                organization_id=org3.id,
                title='Math Tutor',
                description='Help elementary and middle school students with math homework.',
                location='Community Center, 789 Elm St',
                duration=2
            ),
            Opportunity(
                organization_id=org3.id,
                title='Reading Buddy',
                description='Read with young students and help improve literacy skills.',
                location='Public Library, 321 Book Lane',
                duration=1
            ),
            Opportunity(
                organization_id=org1.id,
                title='Community Garden Helper',
                description='Help maintain the community garden and grow fresh vegetables.',
                location='Community Garden, 567 Green Way',
                duration=5
            ),
            Opportunity(
                organization_id=org2.id,
                title='Event Volunteer',
                description='Help at fundraising events for the animal shelter.',
                location='Various event venues',
                duration=6
            )
        ]
        
        db.session.add_all(opportunities)
        db.session.commit()
        
        print(f"Successfully seeded {len(opportunities)} volunteer opportunities across 3 organizations.")


if __name__ == '__main__':
    seed_opportunities()
