from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db
from models import User, Organization, Opportunity, Application, Payment

# --------------------
# App setup
# --------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///volunteer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "super-secret-key"

# Enable CORS
CORS(app)

# Initialize db and migrations
db.init_app(app)
migrate = Migrate(app, db)

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
    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
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
    if request.method == "GET":
        return jsonify([o.to_dict() for o in Organization.query.all()])

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
@app.route("/opportunities", methods=["GET", "POST"])
def opportunities():
    if request.method == "GET":
        return jsonify([o.to_dict() for o in Opportunity.query.all()])

    data = request.get_json()
    opp = Opportunity(
        title=data["title"],
        description=data.get("description"),
        location=data.get("location"),
        duration=data.get("duration"),
        organization_id=data["organization_id"]
    )
    db.session.add(opp)
    db.session.commit()
    return jsonify({"message": "Opportunity created"}), 201

# ---------- APPLICATIONS ----------
@app.route("/applications", methods=["POST"])
def apply():
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
    data = request.get_json()
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

