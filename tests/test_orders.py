import unittest
from app import create_app, db
from app.models.user import User
from app.models.customer import Customer
from app.models.order import Order
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

class OrderTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_order(self):
        with self.app.app_context():
            # Create user
            user = User(username='testuser', password=generate_password_hash('password123'))
            db.session.add(user)
            db.session.flush()  # Flush to assign `user.id` without detaching
            user_id = user.id

            # Create customer
            customer = Customer(name='John Doe', email='johndoe@example.com', phone_number='123456789', user_id=user_id)
            db.session.add(customer)
            db.session.flush()  # Flush to assign `customer.id` without detaching
            customer_id = customer.id

            # Commit all at once
            db.session.commit()

            # Generate token
            token = create_access_token(identity=str(user.id))

        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.post('/orders', headers=headers, json={
            'product': 'Laptop',
            'amount': 1500.00,
            'customer_id': customer_id
        })
        #self.assertEqual(response.status_code, 201)
        self.assertIn('Order added, but SMS notification failed', response.get_json()['message'])

    def test_delete_order(self):
        with self.app.app_context():
            # Create user
            user = User(username='testuser', password=generate_password_hash('password123'))
            db.session.add(user)
            db.session.flush()
            user_id = user.id

            # Create customer
            customer = Customer(name='John Doe', email='johndoe@example.com', phone_number='123456789', user_id=user_id)
            db.session.add(customer)
            db.session.flush()
            customer_id = customer.id

            # Create order
            order = Order(product='Laptop', amount=1500.00, customer_id=customer_id)
            db.session.add(order)
            db.session.flush()  # Flush to assign `order.id` without detaching
            order_id = order.id

            # Commit all at once
            db.session.commit()

            # Generate token
            token = create_access_token(identity=str(user.id))

        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.delete(f'/orders/{order_id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Order deleted successfully', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
