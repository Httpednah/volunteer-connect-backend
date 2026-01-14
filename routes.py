"""
API Routes for Volunteer Connect
"""
from flask import Blueprint, jsonify, request
from app import app, db
from models import Opportunity


opportunities_bp = Blueprint('opportunities', __name__)


@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    """Get all volunteer opportunities"""
    opportunities = Opportunity.query.all()
    return jsonify([opp.to_dict() for opp in opportunities]), 200


@app.route('/opportunities', methods=['POST'])
def create_opportunity():
    """Create a new volunteer opportunity"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    new_opportunity = Opportunity(
        organization_id=data.get('organization_id'),
        title=data.get('title'),
        description=data.get('description'),
        location=data.get('location'),
        duration=data.get('duration')
    )
    
    db.session.add(new_opportunity)
    db.session.commit()
    
    return jsonify(new_opportunity.to_dict()), 201


@app.route('/opportunities/<int:opportunity_id>', methods=['PATCH'])
def update_opportunity(opportunity_id):
    """Update an existing volunteer opportunity"""
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    
    if 'organization_id' in data:
        opportunity.organization_id = data['organization_id']
    if 'title' in data:
        opportunity.title = data['title']
    if 'description' in data:
        opportunity.description = data['description']
    if 'location' in data:
        opportunity.location = data['location']
    if 'duration' in data:
        opportunity.duration = data['duration']
    
    db.session.commit()
    
    return jsonify(opportunity.to_dict()), 200


@app.route('/opportunities/<int:opportunity_id>', methods=['DELETE'])
def delete_opportunity(opportunity_id):
    """Delete a volunteer opportunity"""
    opportunity = Opportunity.query.get_or_404(opportunity_id)
    
    db.session.delete(opportunity)
    db.session.commit()
    
    return jsonify({'message': 'Opportunity deleted successfully'}), 200

