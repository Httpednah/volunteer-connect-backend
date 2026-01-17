from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from datetime import datetime

# Initialize the SQLAlchemy extension
# This object 'db' will be used to interact with the database (create tables, query data, etc.)
db = SQLAlchemy()

# User Model
# Represents a user in our system.
# Inherits from db.Model (standard Flask-SQLAlchemy model) 
# and SerializerMixin (helper to convert model objects to dictionaries for JSON responses)
class User(db.Model, SerializerMixin):
    # This specifies the name of the table in the database
    __tablename__ = 'users'

    # Define columns (fields) for the User table
    # db.Column: Defines a column
    # db.Integer / db.String: Defines the data type
    # primary_key=True: Unique identifier for each record
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    # Add other user fields as needed

    # Relationships linked to other tables
    # 'User' is related to 'Payment'. 'back_populates' creates a link on the Payment model back to User.
    # cascade='all, delete-orphan': If a User is deleted, delete all their Payments too.
    payments = db.relationship('Payment', back_populates='user', cascade='all, delete-orphan')

    # serialize_rules: Prevents infinite loops when converting to JSON.
    # '-payments.user' means: when converting a User's payments to JSON, don't include the 'user' field inside those payments again.
    serialize_rules = ('-payments.user',)

# -------------------------------------------------------------------
# Opportunity Model
# Represents a volunteering opportunity.
# -------------------------------------------------------------------
class Opportunity(db.Model, SerializerMixin):
    __tablename__ = 'opportunities'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    # Add other opportunity fields as needed

    # Relationship to Payment
    payments = db.relationship('Payment', back_populates='opportunity', cascade='all, delete-orphan')

    serialize_rules = ('-payments.opportunity',)

# -------------------------------------------------------------------
# Payment Model
# Represents a payment made by a User for an Opportunity.
# -------------------------------------------------------------------
class Payment(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    # Primary Key
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign Keys
    # Links this payment to a specific User and Opportunity by their ID.
    # nullable=False: A payment MUST belong to a user and an opportunity.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey('opportunities.id'), nullable=False)
    
    # Data Fields
    amount = db.Column(db.Float, nullable=False)
    # pending, completed, or failed
    payment_status = db.Column(db.String(20), nullable=False, default='pending') 
    # Automatically set to the current time when created
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    # Allows us to access the actual User/Opportunity objects (e.g., payment.user.username)
    user = db.relationship('User', back_populates='payments')
    opportunity = db.relationship('Opportunity', back_populates='payments')

    # Exclude recursive fields from JSON serialization
    serialize_rules = ('-user.payments', '-opportunity.payments')

    # -------------------------------------------------------------------
    # Validations
    # These functions run automatically to check data validity before saving to the DB.
    # -------------------------------------------------------------------

    @validates('payment_status')
    def validate_status(self, key, status):
        """Ensure payment_status is one of the allowed values."""
        valid_statuses = ['pending', 'completed', 'failed']
        if status not in valid_statuses:
            raise ValueError(f"Status must be one of {', '.join(valid_statuses)}")
        return status

    @validates('amount')
    def validate_amount(self, key, amount):
        """Ensure amount is a positive number."""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        return amount

    def __repr__(self):
        """String representation of the object for debugging."""
        return f'<Payment {self.id} - {self.amount} ({self.payment_status})>'
