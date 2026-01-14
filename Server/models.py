from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(
    naming_convention={
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    }
)

db = SQLAlchemy(metadata=metadata)

# User model
class User(db.Model, SerializerMixin):
    __tablename__ = "users"
    serialize_rules = ("-organizations.owner",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    organizations = db.relationship(
        "Organization",
        back_populates="owner",
        cascade="all, delete"
    )

# Organization model
class Organization(db.Model, SerializerMixin):
    __tablename__ = "organizations"
    serialize_rules = ("-owner.organizations",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    location = db.Column(db.String)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    owner = db.relationship("User", back_populates="organizations")

    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
