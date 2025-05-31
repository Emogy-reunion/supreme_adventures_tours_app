from app.models import Users, Profiles, db
from app import create_app
from sqlalchemy import or_
from dotenv import load_dotenv
import os


load_dotenv()

def create_initial_admin():
    app = create_app()

    with app.app_context():
        try:
            admin = {
                    'email': os.getenv('ADMIN_EMAIL'),
                    'username': os.getenv('ADMIN_USERNAME'),
                    'phone_number': os.getenv('ADMIN_PHONE'),
                    'first_name': os.getenv('ADMIN_FIRST_NAME'),
                    'last_name': os.getenv('ADMIN_LAST_NAME'),
                    'password': os.getenv('ADMIN_PASSWORD'),
                    }
            admin_exists = Users.query.filter(
                    or_(Users.email == admin['email'], Users.username == admin['username'])
                    ).first()

            if admin_exists:
                return {"error": 'The initial admin already exists!'}
            else:
                initial_admin = Users(
                        email=admin['email'],
                        username=admin['username'],
                        phone_number=admin['phone_number'],
                        password=admin['password']
                        )

                initial_admin.role = 'admin';
                db.session.flush()

                admin_profile = Profiles(
                        first_name=admin['first_name'],
                        last_name=admin['last_name'],
                        user_id=initial_admin.id
                        )
                db.session.commit()
                return {'success': 'Admin created successfully!'}
        except Exception as e:
            db.session.rollback()
            return {'error': 'An unexpected error occured. Please try again!'}
