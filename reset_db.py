from app import app
from extensions import db

with app.app_context():
    db.drop_all()  # drop old tables if they exist
    db.create_all()  # create tables fresh from models
    print("Database reset complete!")

