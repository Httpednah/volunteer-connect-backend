from flask import Flask, request, make_response
from flask_migrate import Migrate
from models import db, User, Organization

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def home():
    return "<h1>Volunteer Connect API</h1>"

# GET all organizations 
@app.route("/organizations", methods=["GET"])
def get_organizations():
    orgs = Organization.query.all()
    return make_response([org.to_dict() for org in orgs], 200)

# POST create organization 
@app.route("/organizations", methods=["POST"])
def create_organization():
    data = request.get_json()
    
    # Validation: name is required
    if not data.get("name"):
        return make_response({"error": "Organization name is required"}, 400)

    org = Organization(
        name=data["name"],
        description=data.get("description"),
        location=data.get("location"),
        owner_id=data.get("owner_id")
    )

    db.session.add(org)
    db.session.commit()

    return make_response(org.to_dict(), 201)


if __name__ == "__main__":
    app.run(port=5555, debug=True)

