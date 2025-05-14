from flask_sqlalchemy import SQLAlchemy
from . import create_app
from datetime import datetime
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer


app = create_app()
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


class Users(db.Model):
    '''
    table that stores user authentication details
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), uniques=True, nullable=False)
    phone_number = db.Column(db.String(12), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default='member', nullable=True)
    verified = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('Profiles', uselist=False, backref='user', lazy='selectin')

    def __init__(self, email, username, phone_number, password):
        self.email = email
        self.username = username
        self.phone_number = phone_number
        self.password_hash = generate_password_hash(password)

    def generate_password_hash(self, password):
        '''
        hashes the password
        '''
        return bcrypt.generate_password_hash(hash)
    
    def check_password(self, password):
        '''
        compares the password with the stored hash
        return true if there is a match else false
        '''
        return bcrypt.check_password_hash(self.password, password)

    def email_verification_token(self):
    '''
    serializes the user id that will be used to verify the user
    '''
        return serializer.dumps({'user_id': self.id}, expires_in=3600)
    
    @staticmethod
    def verify_token(token):
        '''
        deserializes the token and retrieves the user id
        queries the database and retrieves the user if they exist
        '''
        try:
            data = serializer.loads(token)
            user = db.session.get(Users, data['user_id'])
            if user:
                return user
            else:
                return None
        except Exception as e:
            return None


class Profiles(db.Model):
    '''
    stores the user's profile information
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    profile_picture = db.Column(db.String(200), nullable=True, default='default.jpg')

    def __init__(self, user_id, first_name, last_name):
        '''
        initializes the table columns with data
        '''
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
