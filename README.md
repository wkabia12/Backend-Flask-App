# Flask Application for User, Customer, and Order Management

This Flask application provides APIs for managing users, customers, and orders. It supports user authentication, customer management, and order processing, including sending notifications via SMS (using Africa's Talking).

## Features

- **User Management**: 
  - User registration and authentication using JWT.
  - View all users.
  - Delete a user and their associated data.

- **Customer Management**:
  - Add, view, and delete customers associated with a user.

- **Order Management**:
  - Create, view, and delete orders associated with customers.
  - SMS notification for new orders (via Africa's Talking).

---

## Technologies Used

- **Backend**: Flask, Flask SQLAlchemy, Flask JWT-Extended.
- **Database**: SQLite (default), but supports PostgreSQL and other databases.
- **Migrations**: Flask-Migrate.
- **SMS Notifications**: Africa's Talking API.
- **Testing**: Python `unittest`.

---

## Prerequisites

1. **Python**: Ensure you have Python 3.10 or later installed.
2. **Database**: SQLite is included by default. For production, configure a PostgreSQL or other database.
3. **Africa's Talking API Key**: Required for sending SMS.

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/your-flask-app.git
cd your-flask-app
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root of your project and configure the following:
```
DATABASE_URL=sqlite:///app.db
JWT_SECRET_KEY=your_jwt_secret_key
AFRICASTALKING_USERNAME=sandbox
AFRICASTALKING_API_KEY=your_africas_talking_api_key
```

### 5. Run Migrations
```bash
flask db upgrade
```

### 6. Start the Application
```bash
python run.py
```

---

## API Endpoints

### User Endpoints
| Method | Endpoint          | Description                    | Authentication |
|--------|-------------------|--------------------------------|----------------|
| POST   | `/register`       | Register a new user            | No             |
| POST   | `/login`          | Authenticate and get JWT token | No             |
| GET    | `/users`          | View all users                 | Yes            |
| DELETE | `/users/<user_id>`| Delete a user                  | Yes            |

### Customer Endpoints
| Method | Endpoint                | Description                       | Authentication |
|--------|-------------------------|-----------------------------------|----------------|
| POST   | `/customers`            | Add a new customer                | Yes            |
| GET    | `/customers`            | View all customers for a user     | Yes            |
| DELETE | `/customers/<customer_id>` | Delete a customer                 | Yes            |

### Order Endpoints
| Method | Endpoint              | Description                        | Authentication |
|--------|-----------------------|------------------------------------|----------------|
| POST   | `/orders`             | Create a new order                 | Yes            |
| GET    | `/orders`             | View all orders                    | Yes            |
| DELETE | `/orders/<order_id>`  | Delete an order                    | Yes            |

---

## Running Tests
To run the tests, use:
```bash
python3 -m unittest discover tests
```

---