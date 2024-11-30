#Defines Routes for Orders
from flask import Blueprint, request, jsonify
from app.models.order import db, Order
from flask_jwt_extended import jwt_required

bp = Blueprint('order', __name__, url_prefix='')

@bp.route('/orders', methods=['POST'])
@jwt_required()
def add_order():
    data = request.get_json()
    new_order = Order(
        product=data['product'],
        amount=data['amount'],
        customer_id=data['customer_id']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Order added successfully'}), 201


@bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Order.query.all()
    return jsonify([{
        'id': o.id,
        'product': o.product,
        'amount': o.amount,
        'customer_id': o.customer_id
    } for o in orders])