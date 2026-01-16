"""
Database Models for Volunteer Connect

This module defines the SQLAlchemy models representing the application's data entities:
Users, Organizations, Opportunities, Applications, and Payments.
"""
from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# --------------------------
# User Model
# --------------------------
class User(db.Model):
    """
    User model representing individuals in the system.
    Users can have roles of 'volunteer' or 'organization'.
    """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)  # volunteer | organization
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    organizations = db.relationship("Organization", backref="owner", cascade="all, delete")
    applications = db.relationship("Application", backref="user", cascade="all, delete")
    payments = db.relationship("Payment", backref="user", cascade="all, delete")

    def set_password(self, password):
        """Hashes the password and stores it."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifies the provided password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Serializes the user object for JSON responses."""
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
    Organization model representing groups offering volunteer opportunities.
    Each organization is owned by a User with the 'organization' role.
    """
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    opportunities = db.relationship("Opportunity", backref="organization", cascade="all, delete")

    def to_dict(self):
        """Serializes the organization object for JSON responses."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Opportunity(db.Model):
    """
    Opportunity model representing specific volunteer events or roles.
    """
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    duration = db.Column(db.Integer)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship("Application", backref="opportunity", cascade="all, delete")
    payments = db.relationship("Payment", backref="opportunity", cascade="all, delete")

    def to_dict(self):
        """Serializes the opportunity object for JSON responses."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "duration": self.duration,
            "organization_id": self.organization_id,
            "created_by": self.created_by,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Application(db.Model):
    """
    Application model representing a volunteer's interest in an opportunity.
    Used for the application lifecycle (pending, accepted, rejected).
    """
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunities.id"), nullable=False)
    motivation_message = db.Column(db.Text)
    status = db.Column(db.String, default="pending")  # pending | accepted | rejected
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Serializes the application object for JSON responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "opportunity_id": self.opportunity_id,
            "motivation_message": self.motivation_message,
            "status": self.status,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None
        }


class Payment(db.Model):
    """
    Payment model for tracking donations or fees related to opportunities.
    """
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunities.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String, default="pending")  # pending | completed | failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """Serializes the payment object for JSON responses."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "opportunity_id": self.opportunity_id,
            "amount": self.amount,
            "payment_status": self.payment_status,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None
        }
