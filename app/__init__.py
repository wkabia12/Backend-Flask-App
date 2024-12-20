from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os, africastalking

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
# Initialize Africa's Talking
africastalking.initialize(username='sandbox', api_key='atsk_1a795404fcab5ac14bfa7a3d4d7fa0618b16b9bf0cc3c3803b2d4fd5da6632791628f237')
sms = africastalking.SMS

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', '1234567890')  # Change this to a secure secret key
    app.config['JWT_ALGORITHM'] = 'HS256'  # Ensure this matches



    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # Imported Blueprint Endpoints for users, customers and orders

    from app.routes import users, customers, orders
    
    app.register_blueprint(users.bp)
    app.register_blueprint(customers.bp)
    app.register_blueprint(orders.bp)
   

    return app