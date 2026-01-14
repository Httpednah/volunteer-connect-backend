from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    @app.route("/")
    def index():
        return {"message": "Volunteer Connect API running"}

    return app

app = create_app()
