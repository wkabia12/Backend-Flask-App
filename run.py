# Main entry point
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():  # Add this line to push the application context
        db.create_all()  # Create tables in the database

    app.run(debug=True)
