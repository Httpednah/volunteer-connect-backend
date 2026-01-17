"""
Database Models for Volunteer Connect
"""
from extensions import db
from datetime import datetime
from sqlalchemy.orm import validates

# --------------------------
# User Model
# --------------------------
class User(db.Model):
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
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    opportunities = db.relationship("Opportunity", backref="organization", cascade="all, delete")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "location": self.location,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


# --------------------------
# Opportunity Model
# --------------------------
class Opportunity(db.Model):
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    duration = db.Column(db.Integer)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    applications = db.relationship("Application", backref="opportunity", cascade="all, delete")
    payments = db.relationship("Payment", backref="opportunity", cascade="all, delete")

    def to_dict(self):
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


# --------------------------
# Application Model
# --------------------------
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunities.id"), nullable=False)
    motivation_message = db.Column(db.Text)
    status = db.Column(db.String, default="pending")  # pending | accepted | rejected
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
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunities.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String, default="pending")  # pending | completed | failed
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    @validates('payment_status')
    def validate_status(self, key, status):
        valid_statuses = ['pending', 'completed', 'failed']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {', '.join(valid_statuses)}")
        return status

    @validates('amount')
    def validate_amount(self, key, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "opportunity_id": self.opportunity_id,
            "amount": self.amount,
            "payment_status": self.payment_status,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None
        }
