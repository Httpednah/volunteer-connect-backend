from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from models import User, Organization, Opportunity, Application, Payment

# --------------------
# App setup
# --------------------
app = Flask(__name__)

# Configure the SQLite database URI and disable modification tracking for performance
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///volunteer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Enable Cross-Origin Resource Sharing (CORS) for all routes
CORS(app)

# Initialize the database and migration engine
db.init_app(app)
migrate = Migrate(app, db)

# --------------------
# Routes
# --------------------

@app.route("/")
def home():
    """Welcome endpoint to verify the API is running."""
    return jsonify({"message": "Group 5 Volunteer Connect API running"})


# ---------- AUTHENTICATION ----------
@app.route("/register", methods=["POST"])
def register():
    """Registers a new user (Volunteer or Organization)."""
    data = request.get_json()

    # Check for required fields in the request body
    if not all(k in data for k in ("name", "email", "password", "role")):
        return jsonify({"error": "Missing fields"}), 400

    # Ensure the email is unique in the database
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    # Create a new User instance and hash the password
    user = User(
        name=data["name"],
        email=data["email"],
        role=data["role"]
    )
    user.set_password(data["password"])

    # Persist the user to the database
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201


@app.route("/login", methods=["POST"])
def login():
    """Authenticates a user and returns their profile details."""
    data = request.get_json()

    # Find the user by email and verify the password hash
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not user.check_password(data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "id": user.id,
        "name": user.name,
        "role": user.role
    })


# ---------- ORGANIZATIONS ----------
@app.route("/organizations", methods=["GET", "POST"])
def organizations():
    """Handles listing all organizations and creating a new one."""
    if request.method == "GET":
        # Return a list of all organizations with limited fields
        return jsonify([
            {
                "id": o.id,
                "name": o.name,
                "location": o.location
            } for o in Organization.query.all()
        ])

    # For POST requests, create a new organization record
    data = request.get_json()
    org = Organization(
        name=data["name"],
        description=data.get("description"),
        location=data.get("location"),
        owner_id=data["owner_id"]
    )
    db.session.add(org)
    db.session.commit()
    return jsonify({"message": "Organization created"}), 201


# ---------- OPPORTUNITIES ----------
@app.route('/opportunities', methods=['GET'])
def get_opportunities():
    """
    GET /opportunities
    Retrieve all volunteer opportunities from the database.
    """
    opportunities = Opportunity.query.all()
    return jsonify([opp.to_dict() for opp in opportunities]), 200


@app.route('/opportunities', methods=['POST'])
def create_opportunity():
    """
    POST /opportunities
    Create a new volunteer opportunity.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    # Validate required fields
    if not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400

    # Validate duration is numeric if provided
    duration = data.get('duration')
    if duration and not str(duration).replace('.', '').replace('-', '').isdigit():
        return jsonify({'error': 'Duration must be a numeric value'}), 400

    new_opportunity = Opportunity(
        organization_id=data.get('organization_id'),
        title=data.get('title'),
        description=data.get('description'),
        location=data.get('location'),
        duration=data.get('duration')
    )

    db.session.add(new_opportunity)
    db.session.commit()

    return jsonify(new_opportunity.to_dict()), 201


@app.route('/opportunities/<int:opportunity_id>', methods=['PATCH'])
def update_opportunity(opportunity_id):
    """
    PATCH /opportunities/<id>
    Update an existing volunteer opportunity.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    opportunity = Opportunity.query.get_or_404(opportunity_id)

    if 'organization_id' in data:
        opportunity.organization_id = data['organization_id']
    if 'title' in data:
        opportunity.title = data['title']
    if 'description' in data:
        opportunity.description = data['description']
    if 'location' in data:
        opportunity.location = data['location']
    if 'duration' in data:
        opportunity.duration = data['duration']

    db.session.commit()

    return jsonify(opportunity.to_dict()), 200


@app.route('/opportunities/<int:opportunity_id>', methods=['DELETE'])
def delete_opportunity(opportunity_id):
    """
    DELETE /opportunities/<id>
    Delete a volunteer opportunity from the database.
    """
    opportunity = Opportunity.query.get_or_404(opportunity_id)

    db.session.delete(opportunity)
    db.session.commit()

    return jsonify({'message': 'Opportunity deleted successfully'}), 200


# ---------- APPLICATIONS ----------
@app.route("/applications", methods=["POST"])
def apply():
    """Submits a volunteer application for an opportunity."""
    data = request.get_json()
    appn = Application(
        user_id=data["user_id"],
        opportunity_id=data["opportunity_id"],
        motivation_message=data.get("motivation_message")
    )
    db.session.add(appn)
    db.session.commit()
    return jsonify({"message": "Application submitted"}), 201


# ---------- PAYMENTS ----------
@app.route("/payments", methods=["POST"])
def payments():
    """Records a payment (donation or fee) related to an opportunity."""
    data = request.get_json()
    payment = Payment(
        user_id=data["user_id"],
        opportunity_id=data["opportunity_id"],
        amount=data["amount"]
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({"message": "Payment recorded"}), 201

if __name__ == "__main__":
    app.run(port=5000, debug=True)

