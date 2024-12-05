import unittest
from app import create_app, db
from app.models.user import User
from app.models.customer import Customer
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

class CustomerTests(unittest.TestCase):
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

    def test_delete_customer(self):
        with self.app.app_context():
            # Create a test user
            user = User(username='testuser', password=generate_password_hash('password123'))
            db.session.add(user)
            db.session.flush()  # Flush to get the `user.id` without committing
            user_id = user.id

            # Create a test customer associated with the user
            customer = Customer(name='John Doe', email='johndoe@example.com', phone_number='123456789', user_id=user_id)
            db.session.add(customer)
            db.session.flush()  # Flush to get the `customer.id` without committing
            customer_id = customer.id

            # Commit both objects to the database
            db.session.commit()

            # Generate a JWT token for the user
            token = create_access_token(identity=str(user_id))

        # Define the authorization header with the token
        headers = {'Authorization': f'Bearer {token}'}

        # Send a DELETE request to remove the customer
        response = self.client.delete(f'/customers/{customer_id}', headers=headers)

        # Assert the response status code and message
        self.assertEqual(response.status_code, 200)
        self.assertIn('Customer deleted successfully', response.get_json()['message'])

        # Verify that the customer is no longer in the database
        with self.app.app_context():
            deleted_customer = Customer.query.get(customer_id)
            self.assertIsNone(deleted_customer)

if __name__ == '__main__':
    unittest.main()
