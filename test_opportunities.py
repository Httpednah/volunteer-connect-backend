"""
Test suite for Opportunity API endpoints
"""
import pytest
import sys
sys.path.insert(0, '/home/mariam/Development/code/FLASK/volunteer-connect-backend')

# Avoid circular import by importing after path setup
from app import app, db
from models import Opportunity


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_get_opportunities_empty(client):
    """Test GET /opportunities returns empty list when no opportunities exist"""
    response = client.get('/opportunities')
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_opportunities_with_data(client):
    """Test GET /opportunities returns opportunities when data exists"""
    # Create test opportunity
    with app.app_context():
        opp = Opportunity(
            organization_id='org-123',
            title='Test Opportunity',
            description='Test description',
            location='Test location',
            duration='2 hours'
        )
        db.session.add(opp)
        db.session.commit()
    
    response = client.get('/opportunities')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Test Opportunity'


def test_create_opportunity(client):
    """Test POST /opportunities creates new opportunity"""
    payload = {
        'organization_id': 'org-456',
        'title': 'New Opportunity',
        'description': 'A great volunteer opportunity',
        'location': 'Community Center',
        'duration': '4 hours'
    }
    response = client.post('/opportunities', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'New Opportunity'
    assert data['organization_id'] == 'org-456'


def test_update_opportunity(client):
    """Test PATCH /opportunities/<id> updates an opportunity"""
    # Create opportunity first
    with app.app_context():
        opp = Opportunity(
            organization_id='org-789',
            title='Original Title',
            description='Original description'
        )
        db.session.add(opp)
        db.session.commit()
        opp_id = opp.id
    
    response = client.patch(f'/opportunities/{opp_id}', json={'title': 'Updated Title'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'


def test_delete_opportunity(client):
    """Test DELETE /opportunities/<id> deletes an opportunity"""
    # Create opportunity first
    with app.app_context():
        opp = Opportunity(
            organization_id='org-del',
            title='To Be Deleted'
        )
        db.session.add(opp)
        db.session.commit()
        opp_id = opp.id
    
    response = client.delete(f'/opportunities/{opp_id}')
    assert response.status_code == 200
    
    # Verify it's deleted
    with app.app_context():
        assert Opportunity.query.get(opp_id) is None

