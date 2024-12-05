#The customer model
from app import db

class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(15), nullable=False,  server_default="UNKNOWN")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_customer_user'), nullable=False)  # Associate customer with a user
    orders = db.relationship('Order', backref='customer', cascade="all, delete-orphan", lazy=True)

