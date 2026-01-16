"""
API Routes for Volunteer Connect

This module defines Flask routes for managing volunteer opportunities.
Note: These routes are currently also implemented in app.py for a streamlined setup.
"""
from flask import Blueprint, jsonify, request
from extensions import db
from models import Opportunity


# Blueprint can be used for modularizing routes in larger applications
opportunities_bp = Blueprint('opportunities', __name__)


def register_routes(app):
    """
    Optional helper to register routes if using this file as a module.
    Currently, app.py contains the primary route definitions.
    """
    
    @app.route('/opportunities', methods=['GET'])
    def get_opportunities_list():
        """
        GET /opportunities
        Retrieve all volunteer opportunities from the database.
        """
        opportunities = Opportunity.query.all()
        return jsonify([opp.to_dict() for opp in opportunities]), 200


    @app.route('/opportunities', methods=['POST'])
    def create_new_opportunity():
        """
        POST /opportunities
        Create a new volunteer opportunity with validation.
        """
        data = request.get_json()

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        # Validate required fields
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        # Validate duration is numeric if provided
        duration = data.get('duration')
        if duration and not str(duration).replace('.', '').replace('-', '').isdigit():
            return jsonify({'error': 'Duration must be a numeric value'}), 400

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
    """
    PATCH /opportunities/<id>
    
    Update an existing volunteer opportunity.
    
    Request body can include any of:
        - organization_id: Update the organization reference
        - title: Update the opportunity title
        - description: Update the description
        - location: Update the location
        - duration: Update the duration
    
    Returns:
        200: Updated opportunity data
        404: Opportunity not found
    """
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
    """
    DELETE /opportunities/<id>
    
    Delete a volunteer opportunity from the database.
    
    Returns:
        200: Success message
        404: Opportunity not found
    """
    opportunity = Opportunity.query.get_or_404(opportunity_id)

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({'message': 'Opportunity deleted successfully'}), 200

