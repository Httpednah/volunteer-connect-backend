from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from models import User, Organization, Opportunity, Application, Payment
from werkzeug.security import generate_password_hash, check_password_hash

# --------------------
# App setup
# --------------------
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///volunteer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key"

# Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Initialize db and migrations
db.init_app(app)
migrate = Migrate(app, db)

# --------------------
# Helpers for User password
# --------------------
def set_password(user, password):
    user.password_hash = generate_password_hash(password)

def check_password(user, password):
    return check_password_hash(user.password_hash, password)

# --------------------
# Routes
# --------------------
@app.route("/")
def home():
    return jsonify({"message": "Volunteer Connect API running"})

# ---------- AUTH ----------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    if not all(k in data for k in ("name", "email", "password", "role")):
        return jsonify({"error": "Missing fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "Email already exists"}), 400

    user = User(
        name=data["name"],
        email=data["email"],
        role=data["role"]
    )
    set_password(user, data["password"])

    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
    if not user or not check_password(user, data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "id": user.id,
        "name": user.name,
        "role": user.role
    })

# ---------- ORGANIZATIONS ----------
@app.route("/organizations", methods=["GET", "POST"])
def organizations():
    if request.method == "GET":
        return jsonify([o.to_dict() for o in Organization.query.all()])

    data = request.get_json()
    if not data or not data.get("name") or not data.get("owner_id"):
        return jsonify({"error": "Missing organization name or owner_id"}), 400

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
@app.route("/opportunities", methods=["GET", "POST"])
def opportunities():
    if request.method == "GET":
        return jsonify([o.to_dict() for o in Opportunity.query.all()])

    # POST logic
    data = request.get_json()
    if not data or not data.get("title") or not data.get("organization_id"):
        return jsonify({"error": "Missing title or organization_id"}), 400

    duration = data.get("duration")
    if duration and not isinstance(duration, (int, float)):
        try:
            duration = int(duration)
        except ValueError:
            return jsonify({"error": "Duration must be a number"}), 400

    new_opportunity = Opportunity(
        organization_id=data["organization_id"],
        title=data["title"],
        description=data.get("description"),
        location=data.get("location"),
        duration=duration,
        created_by=data.get("created_by")
    )
    db.session.add(new_opportunity)
    db.session.commit()
    return jsonify(new_opportunity.to_dict()), 201

@app.route("/opportunities/<int:id>", methods=["PATCH"])
def update_opportunity(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    opportunity = Opportunity.query.get_or_404(id)
    for field in ["title", "description", "location", "duration", "organization_id"]:
        if field in data:
            setattr(opportunity, field, data[field])

    db.session.commit()
    return jsonify(opportunity.to_dict()), 200

@app.route("/opportunities/<int:id>", methods=["DELETE"])
def delete_opportunity(id):
    opportunity = Opportunity.query.get_or_404(id)
    db.session.delete(opportunity)
    db.session.commit()
    return jsonify({"message": "Opportunity deleted successfully"}), 200

# ---------- APPLICATIONS ----------
@app.route("/applications", methods=["POST"])
def apply():
    data = request.get_json()
    if not data or not data.get("user_id") or not data.get("opportunity_id"):
        return jsonify({"error": "Missing user_id or opportunity_id"}), 400

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
    data = request.get_json()
    if not data or not data.get("user_id") or not data.get("opportunity_id") or not data.get("amount"):
        return jsonify({"error": "Missing fields"}), 400

    payment = Payment(
        user_id=data["user_id"],
        opportunity_id=data["opportunity_id"],
        amount=data["amount"]
    )
    db.session.add(payment)
    db.session.commit()
    return jsonify({"message": "Payment recorded"}), 201

# --------------------
# Run App
# --------------------
if __name__ == "__main__":
    app.run(debug=True)
