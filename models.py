"""
Database Models for Volunteer Connect

This module defines all SQLAlchemy models for the application.
"""
from app import db
from datetime import datetime
import uuid
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# --------------------------
# User Model
# --------------------------
class User(db.Model):
    """
    User model representing volunteers or organization owners.

    Attributes:
        id: Unique identifier (UUID string)
        name: Full name
        email: Email address
        password_hash: Hashed password
        role: "volunteer" or "organization"
        created_at: Account creation timestamp
    """
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # volunteer | organization
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    organizations = db.relationship("Organization", backref="owner", cascade="all, delete-orphan")
    applications = db.relationship("Application", backref="user", cascade="all, delete-orphan")
    payments = db.relationship("Payment", backref="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

# --------------------------
# Organization Model
# --------------------------
class Organization(db.Model):
    """
    Organization model representing organizations that post volunteer opportunities.

    Attributes:
        id: Unique identifier (UUID string)
        name: Organization's display name
        owner_id: User ID of the organization owner
    """
    __tablename__ = 'organizations'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    opportunities = db.relationship("Opportunity", backref="organization", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'owner_id': self.owner_id
        }

# --------------------------
# Opportunity Model
# --------------------------
class Opportunity(db.Model):
    """
    Opportunity model representing volunteer opportunities posted by organizations.
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
    created_by = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=True)

    applications = db.relationship("Application", backref="opportunity", cascade="all, delete-orphan")
    payments = db.relationship("Payment", backref="opportunity", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'organization_id': self.organization_id,
            'title': self.title,
            'description': self.description,
            'location': self.location,
            'duration': self.duration,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'created_by': self.created_by
        }

# --------------------------
# Application Model (Many-to-Many)
# --------------------------
class Application(db.Model):
    """
    Application model linking users to opportunities.
    """
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    motivation_message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="pending")  # pending | accepted | rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "opportunity_id": self.opportunity_id,
            "motivation_message": self.motivation_message,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None
        }

# --------------------------
# Payment Model
# --------------------------
class Payment(db.Model):
    """
    Payment model linking users to opportunities.
    """
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    amount = db.Column(db.Numeric(10,2), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False, default="pending")  # pending | completed | failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "opportunity_id": self.opportunity_id,
            "amount": str(self.amount),
            "payment_status": self.payment_status,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None
        }
