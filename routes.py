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

