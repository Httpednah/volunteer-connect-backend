"""
Seed data for Volunteer Connect database
"""

from app import app, db
from models import Organization, Opportunity


def seed_opportunities():
    """Add sample volunteer opportunities"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create sample organizations
        org1 = Organization(name='Local Food Bank')
        org2 = Organization(name='Animal Shelter')
        org3 = Organization(name='Youth Mentoring Program')
        
        db.session.add_all([org1, org2, org3])
        db.session.commit()  # IDs are generated here
        
        # Create sample opportunities
        opportunities = [
            Opportunity(
                organization_id=org1.id,
                title='Food Sorting Helper',
                description='Help sort and package food donations for families in need. No experience necessary, training provided.',
                location='Downtown Food Bank, 123 Main St',
                duration=4
            ),
            Opportunity(
                organization_id=org1.id,
                title='Delivery Driver',
                description='Deliver food packages to elderly and disabled residents in our community.',
                location='Various locations',
                duration=3
            ),
            Opportunity(
                organization_id=org2.id,
                title='Dog Walker',
                description='Walk shelter dogs to keep them healthy and happy. Must be comfortable with animals.',
                location='City Animal Shelter, 456 Oak Ave',
                duration=2
            ),
            Opportunity(
                organization_id=org2.id,
                title='Cat Caretaker',
                description='Feed, groom, and socialize cats at the shelter. Great for cat lovers!',
                location='City Animal Shelter, 456 Oak Ave',
                duration=3
            ),
            Opportunity(
                organization_id=org3.id,
                title='Math Tutor',
                description='Help elementary and middle school students with math homework. Make a difference in their education!',
                location='Community Center, 789 Elm St',
                duration=2
            ),
            Opportunity(
                organization_id=org3.id,
                title='Reading Buddy',
                description='Read with young students and help improve their literacy skills. Flexible scheduling available.',
                location='Public Library, 321 Book Lane',
                duration=1
            ),
            Opportunity(
                organization_id=org1.id,
                title='Community Garden Helper',
                description='Help maintain the community garden and grow fresh vegetables for the food bank.',
                location='Community Garden, 567 Green Way',
                duration=5
            ),
            Opportunity(
                organization_id=org2.id,
                title='Event Volunteer',
                description='Help at fundraising events for the animal shelter. Tasks include registration, refreshments, and setup.',
                location='Various event venues',
                duration=6
            )
        ]
        
        db.session.add_all(opportunities)
        db.session.commit()
        
        print(f"Seeded {len(opportunities)} volunteer opportunities across 3 organizations")


if __name__ == '__main__':
    seed_opportunities()
