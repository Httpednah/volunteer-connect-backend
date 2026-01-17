from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# --------------------
# App setup
# --------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///volunteer.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

CORS(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# --------------------
# Models
# --------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    organizations = db.relationship("Organization", backref="owner", cascade="all, delete")
    applications = db.relationship("Application", backref="user", cascade="all, delete")
    payments = db.relationship("Payment", backref="user", cascade="all, delete")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Organization(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    opportunities = db.relationship("Opportunity", backref="organization", cascade="all, delete")


class Opportunity(db.Model):
    __tablename__ = "opportunities"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String)
    duration = db.Column(db.Integer)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)
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
            "created_at": self.created_at.isoformat() if self.created_at else None
        }


class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunities.id"), nullable=False)
    motivation_message = db.Column(db.Text)
    status = db.Column(db.String, default="pending")
    applied_at = db.Column(db.DateTime, default=datetime.utcnow)


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    opportunity_id = db.Column(db.Integer, db.ForeignKey("opportunities.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String, default="pending")
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)


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

    user = User(name=data["name"], email=data["email"], role=data["role"])
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
    return jsonify({"id": user.id, "name": user.name, "role": user.role})


# ---------- ORGANIZATIONS ----------
@app.route("/organizations", methods=["GET", "POST"])
def organizations():
    if request.method == "GET":
        return jsonify([{"id": o.id, "name": o.name, "location": o.location} for o in Organization.query.all()])
    
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
    if not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    duration = data.get("duration")
    if duration is not None:
        try:
            duration = int(duration)
        except (ValueError, TypeError):
            return jsonify({"error": "Duration must be a numeric value"}), 400

    opp = Opportunity(
        title=data["title"],
        description=data.get("description"),
        location=data.get("location"),
        duration=duration,
        organization_id=data.get("organization_id")
    )
    db.session.add(opp)
    db.session.commit()
    return jsonify(opp.to_dict()), 201


@app.route("/opportunities/<int:id>", methods=["PATCH"])
def update_opportunity(id):
    opp = Opportunity.query.get_or_404(id)
    data = request.get_json()
    for field in ["title", "description", "location", "duration"]:
        if field in data:
            setattr(opp, field, data[field])
    db.session.commit()
    return jsonify(opp.to_dict()), 200


@app.route("/opportunities/<int:id>", methods=["DELETE"])
def delete_opportunity(id):
    opp = Opportunity.query.get_or_404(id)
    db.session.delete(opp)
    db.session.commit()
    return jsonify({"message": "Opportunity deleted"}), 200


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


if __name__ == "__main__":
    app.run(debug=True)
