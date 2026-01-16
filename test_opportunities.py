"""
Test suite for Opportunity API endpoints
"""
import pytest
from app import app
from extensions import db
from models import Organization, Opportunity, User


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


def create_test_org():
    """Helper to create a test organization"""
    user = User.query.filter_by(email="test@example.com").first()
    if not user:
        user = User(name="Test User", email="test@example.com", role="organization")
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        
    org = Organization(name='Test Org', owner_id=user.id)
    db.session.add(org)
    db.session.commit()
    return org


def test_get_opportunities_empty(client):
    """GET /opportunities returns empty list when no opportunities exist"""
    response = client.get('/opportunities')
    assert response.status_code == 200
    assert response.get_json() == []


def test_get_opportunities_with_data(client):
    """GET /opportunities returns opportunities when data exists"""
    with app.app_context():
        org = create_test_org()
        opp = Opportunity(
            organization_id=org.id,
            title='Test Opportunity',
            description='Test description',
            location='Test location',
            duration=2
        )
        db.session.add(opp)
        db.session.commit()

    response = client.get('/opportunities')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['title'] == 'Test Opportunity'


def test_create_opportunity(client):
    """POST /opportunities creates new opportunity"""
    with app.app_context():
        org = create_test_org()
        org_id = org.id

    payload = {
        'organization_id': org_id,
        'title': 'New Opportunity',
        'description': 'A great volunteer opportunity',
        'location': 'Community Center',
        'duration': 4
    }
    response = client.post('/opportunities', json=payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'New Opportunity'
    assert data['organization_id'] == org_id


def test_update_opportunity(client):
    """PATCH /opportunities/<id> updates an opportunity"""
    with app.app_context():
        org = create_test_org()
        opp = Opportunity(
            organization_id=org.id,
            title='Original Title',
            description='Original description',
            duration=2
        )
        db.session.add(opp)
        db.session.commit()
        opp_id = opp.id

    response = client.patch(f'/opportunities/{opp_id}', json={'title': 'Updated Title'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['title'] == 'Updated Title'


def test_delete_opportunity(client):
    """DELETE /opportunities/<id> deletes an opportunity"""
    with app.app_context():
        org = create_test_org()
        opp = Opportunity(
            organization_id=org.id,
            title='To Be Deleted',
            duration=2
        )
        db.session.add(opp)
        db.session.commit()
        opp_id = opp.id

    response = client.delete(f'/opportunities/{opp_id}')
    assert response.status_code == 200

    with app.app_context():
        assert Opportunity.query.get(opp_id) is None


def test_create_opportunity_without_title(client):
    """POST /opportunities returns error when title is missing"""
    with app.app_context():
        org = create_test_org()
        org_id = org.id

    payload = {
        'organization_id': org_id,
        'description': 'No title provided',
        'location': 'Test location',
        'duration': 2
    }
    response = client.post('/opportunities', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'Title is required' in data['error']


def test_create_opportunity_invalid_duration(client):
    """POST /opportunities returns error when duration is not numeric"""
    with app.app_context():
        org = create_test_org()
        org_id = org.id

    payload = {
        'organization_id': org_id,
        'title': 'Test Opportunity',
        'duration': 'not-a-number'
    }
    response = client.post('/opportunities', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert 'Duration must be a numeric value' in data['error']
