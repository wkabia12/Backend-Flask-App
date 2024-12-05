import unittest
from app import create_app, db
from app.models.user import User
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash

class UserTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.drop_all()  # Drop existing tables
            db.create_all()  # Recreate tables

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        response = self.client.post('/register', json={
            'username': 'testuser',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_json()['message'])

    def test_login_user(self):
        with self.app.app_context():
            user = User(username='testuser', password=generate_password_hash('password123'))
            db.session.add(user)
            db.session.commit()

        response = self.client.post('/login', json={
            'username': 'testuser',
            'password': 'password123'  # Pass the plaintext password
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.get_json())

    def test_get_all_users(self):
        with self.app.app_context():
            user = User(username='testuser', password=generate_password_hash('password123'))
            db.session.add(user)
            db.session.commit()

            token = create_access_token(identity=str(user.id))

        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.get('/users', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        with self.app.app_context():
            user = User(username='testuser', password=generate_password_hash('password123'))
            db.session.add(user)
            db.session.commit()

            token = create_access_token(identity=str(user.id))

        headers = {'Authorization': f'Bearer {token}'}
        response = self.client.delete(f'/users/{user.id}', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertIn('User and associated records deleted successfully', response.get_json()['message'])

if __name__ == '__main__':
    unittest.main()
