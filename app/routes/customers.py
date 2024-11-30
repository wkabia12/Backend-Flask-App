#Defines Routes for Customers
from flask import Blueprint, request, jsonify
from app.models.customer import db, Customer
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('customer', __name__, url_prefix='')

@bp.route('/customers', methods=['POST'])
@jwt_required()
def add_customer():
    current_user_id = get_jwt_identity()  # Retrieve user ID from the token
    data = request.get_json()
    new_customer = Customer(name=data['name'], email=data['email'], user_id=current_user_id)
    db.session.add(new_customer)
    db.session.commit()
    return jsonify({'message': 'Customer added successfully'}), 201

@bp.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    current_user_id = get_jwt_identity()  # Retrieve user ID from the token
    customers = Customer.query.filter_by(user_id=current_user_id).all()  # Filter customers by user ID
    return jsonify([{'id': c.id, 'name': c.name, 'email': c.email} for c in customers])