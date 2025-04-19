from flask_sqlalchemy import SQLAlchemy
from create_app import create app
from datetime import datetime


app = create_app()
db = SQLAlchemy(app)


class Users(db.Model):
    '''
    table that stores user details
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), uniques=True, nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='member')
    verified = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

Class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True, default='default.jpg')
