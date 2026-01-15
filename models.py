"""
Database Models for Volunteer Connect

This module defines all SQLAlchemy models for the application.
"""
from app import db
from datetime import datetime


class Organization(db.Model):
    """
    Organization model representing organizations that post volunteer opportunities.
    
    Attributes:
        id: Unique identifier (UUID string)
        name: Organization's display name
    """
    __tablename__ = 'organizations'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    def to_dict(self):
        """Convert organization to dictionary representation"""
        return {
            'id': self.id,
            'name': self.name
        }


class Opportunity(db.Model):
    """
    Opportunity model representing volunteer opportunities posted by organizations.
    
    Attributes:
        id: Unique identifier for the opportunity
        organization_id: Foreign key linking to the posting organization
        title: Brief title of the volunteer opportunity
        description: Detailed description of duties and requirements
        location: Where the opportunity takes place
        duration: Estimated time commitment (in hours)
        created_at: Timestamp when the opportunity was created
        updated_at: Timestamp when the opportunity was last updated
    """
    __tablename__ = 'opportunities'
    
    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(200), nullable=True)
    duration = db.Column(db.String(50), nullable=True)  # e.g., "2 hours", "1 day"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert opportunity to dictionary representation"""
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

