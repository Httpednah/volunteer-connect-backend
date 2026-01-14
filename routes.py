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

