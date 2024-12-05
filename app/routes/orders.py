#Defines Routes for Orders
from flask import Blueprint, request, jsonify
from app.models.order import db, Order
from app.models.customer import db, Customer
from flask_jwt_extended import jwt_required
from app import sms


bp = Blueprint('order', __name__, url_prefix='')

@bp.route('/orders', methods=['POST'])
@jwt_required()
def add_order():
    data = request.get_json()
    customer_id = data['customer_id']

    # Check if the customer exists
    customer = Customer.query.filter_by(id=customer_id).first()
    if not customer:
        return jsonify({'message': 'Customer not found'}), 404

    # Add new order
    new_order = Order(
        product=data['product'],
        amount=data['amount'],
        customer_id=customer_id
    )
    db.session.add(new_order)
    db.session.commit()

    # Send SMS
    try:
        message = f"Hello {customer.name}, your order for {new_order.product} has been received. Amount: {new_order.amount}."
        response = sms.send(message, [customer.phone_number])  # Assuming `phone_number` exists in Customer
        print(response)  # Log the response for debugging
    except Exception as e:
        print(f"Failed to send SMS: {str(e)}")
        return jsonify({'message': 'Order added, but SMS notification failed'}), 500

    return jsonify({'message': 'Order added successfully, and SMS sent to customer'}), 201

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

@bp.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = Order.query.filter_by(id=order_id).first()

    if not order:
        return jsonify({'message': 'Order not found'}), 404

    db.session.delete(order)
    db.session.commit()

    return jsonify({'message': 'Order deleted successfully'}), 200