#Defines Routes for Users
from flask import Blueprint, request, jsonify
from app.models.user import db, User
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user', __name__, url_prefix='')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        # Ensure the user ID is passed as a string, even if it's an integer
        access_token = create_access_token(identity=str(user.id))  # Convert to string
        return jsonify({'access_token': access_token, 'user_id': user.id}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@bp.route('/users', methods=['GET'])
@jwt_required()
def get_all_users():
    users = User.query.all()  # Retrieve all users from the database
    user_list = [
        {'id': user.id, 'username': user.username} for user in users
    ]

    return jsonify(user_list), 200


@bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    current_user_id = get_jwt_identity()
    user_id = str(user_id)
    
    # Ensure the user can only delete their own account
    if user_id != current_user_id:
        return jsonify({'message': 'Unauthorized'}), 403

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User and associated records deleted successfully'}), 200
