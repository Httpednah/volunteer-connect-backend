from flask import Blueprint, request, jsonify, make_response
from models import db, Payment, User, Opportunity

# -------------------------------------------------------------------
# Blueprint Configuration
# A Blueprint allows us to organize related routes together.
# Instead of defining everything in app.py, we define 'payments' routes here.
# -------------------------------------------------------------------
payments_bp = Blueprint('payments', __name__)

# -------------------------------------------------------------------
# GET /payments
# Retrieve a list of all payments in the database.
# -------------------------------------------------------------------
@payments_bp.route('/payments', methods=['GET'])
def get_payments():
    # 1. Query the database for all Payment records
    payments = Payment.query.all()
    
    # 2. Iterate through the list of payments and convert each one to a dictionary
    #    using to_dict() (provided by SerializerMixin).
    payment_list = [payment.to_dict() for payment in payments]
    
    # 3. Return the list as a JSON response with status code 200 (OK)
    return jsonify(payment_list), 200

# -------------------------------------------------------------------
# POST /payments
# Create a new payment record.
# Expects JSON data: { "user_id": 1, "opportunity_id": 1, "amount": 50.0 }
# -------------------------------------------------------------------
@payments_bp.route('/payments', methods=['POST'])
def create_payment():
    # 1. Get the JSON data sent by the user
    data = request.get_json()
    
    # 2. Basic Validation: Check if all necessary fields are present
    if not all(key in data for key in ('user_id', 'opportunity_id', 'amount')):
        return jsonify({'error': 'Missing required fields: user_id, opportunity_id, amount'}), 400
        
    try:
        # 3. Convert amount to float to ensure it's a number
        amount = float(data['amount'])
        
        # 4. Create a new Payment object
        new_payment = Payment(
            user_id=data['user_id'],
            opportunity_id=data['opportunity_id'],
            amount=amount,
            # Use .get() to provide a default value if 'payment_status' is missing
            payment_status=data.get('payment_status', 'pending') 
        )
        
        # 5. Add the new object to the database session and commit (save) it
        db.session.add(new_payment)
        db.session.commit()
        
        # 6. Return the created payment as JSON with status 201 (Created)
        return jsonify(new_payment.to_dict()), 201
        
    except ValueError as e:
         # Handle cases where amount is not a number or validation fails
         return jsonify({'error': str(e)}), 400
    except Exception as e:
        # If any other error occurs (e.g., database error), rollback the session to avoid corruption
        db.session.rollback()
        return jsonify({'error': f"Failed to create payment: {str(e)}"}), 500

# -------------------------------------------------------------------
# PATCH /payments/<id>
# Update an existing payment (e.g., change status or amount).
# <int:id> captures the ID from the URL.
# -------------------------------------------------------------------
@payments_bp.route('/payments/<int:id>', methods=['PATCH'])
def update_payment(id):
    # 1. Find the payment by ID
    payment = Payment.query.get(id)
    
    # 2. If not found, return 404 Error
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
        
    # 3. Get the data to update
    data = request.get_json()
    
    try:
        # 4. Update fields if they are present in the request
        if 'amount' in data:
            payment.amount = float(data['amount'])
        if 'payment_status' in data:
            payment.payment_status = data['payment_status']
        
        # 5. Commit the changes
        db.session.commit()
        
        # 6. Return the updated payment
        return jsonify(payment.to_dict()), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to update payment: {str(e)}"}), 500

# -------------------------------------------------------------------
# DELETE /payments/<id>
# Delete a payment record from the database.
# -------------------------------------------------------------------
@payments_bp.route('/payments/<int:id>', methods=['DELETE'])
def delete_payment(id):
    # 1. Find the payment
    payment = Payment.query.get(id)
    if not payment:
        return jsonify({'error': 'Payment not found'}), 404
        
    try:
        # 2. Delete the record and commit
        db.session.delete(payment)
        db.session.commit()
        
        # 3. Return success message
        return jsonify({'message': 'Payment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f"Failed to delete payment: {str(e)}"}), 500
