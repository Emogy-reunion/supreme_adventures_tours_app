from . import create_app
from datetime import datetime, date
from itsdangerous import URLSafeTimedSerializer
from app import db, bcrypt


app = create_app()
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


class Users(db.Model):
    '''
    table that stores user authentication details
    has a one to one relationship with the Profiles table (one user, one profile)
    has a one to many relationship with Tours table ( one user, many tours)
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    is_superadmin = db.Column(db.Boolean, default=False, nullable=False)
    role = db.Column(db.String(50), default='member', nullable=True)
    verified = db.Column(db.Boolean, default=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    profile = db.relationship('Profiles', uselist=False, backref='user', lazy='selectin', cascade='all, delete')
    tours = db.relationship('Tours', back_populates='user', lazy='selectin')
    products = db.relationship('Products', back_populates='user', lazy='selectin')
    bookings = db.relationship('Bookings', back_populates='user', lazy='selectin')

    def __init__(self, email, username, phone_number, password):
        self.email = email
        self.username = username
        self.phone_number = phone_number
        self.password_hash = self.generate_passwordhash(password)

    def generate_passwordhash(self, password):
        '''
        hashes the password
        '''
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        '''
        compares the password with the stored hash
        return true if there is a match else false
        '''
        return bcrypt.check_password_hash(self.password_hash, password)

    def email_verification_token(self):
        '''
        serializes the user id that will be used to verify the user
        '''
        return serializer.dumps({'user_id': self.id})

    @staticmethod
    def verify_token(token):
        '''
        deserializes the token and retrieves the user id
        queries the database and retrieves the user if they exist
        '''
        try:
            data = serializer.loads(token, max_age=3600)
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
    has a one to one relationship to Users page (one profile belongs to exactly one user
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


class Tours(db.Model):
    '''
    store information about a tour
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    start_location = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    days = db.Column(db.Integer, nullable=False)
    nights = db.Column(db.Integer, nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, nullable=False)
    final_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    included = db.Column(db.Text, nullable=False)
    excluded = db.Column(db.Text, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = db.relationship('Users', back_populates='tours')
    images = db.relationship('TourImages', backref='tour', cascade='all, delete', lazy='selectin')
    poster = db.relationship('Posters', backref='tour', cascade='all, delete', lazy='selectin', uselist=False)
    bookings = db.relationship('Bookings', back_populates='tour', lazy='selectin')

    def __init__(self, user_id, name, start_location, destination, description, start_date, end_date,
                 status, original_price, discount_percent, final_price, included, excluded, days, nights):
        self.user_id = user_id
        self.name = name
        self.start_location = start_location
        self.destination = destination
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.days = days
        self.nights = nights
        self.original_price = original_price
        self.discount_percent = discount_percent
        self.final_price = final_price
        self.included = included
        self.excluded = excluded
        self.status = status

class TourImages(db.Model):
    '''
    store images related to a specific tour
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

    def __init__(self, tour_id, filename):
        self.tour_id = tour_id
        self.filename = filename

class Posters(db.Model):
    '''
    stores a poster related to a specific tour
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False, unique=True)
    poster = db.Column(db.String(100), nullable=False)

class Products(db.Model):
    '''
    stores merchandise sold via the app
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_type = db.Column(db.String(150), nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    discount_rate = db.Column(db.Integer, default=0)
    final_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    size = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    images = db.relationship('ProductImages', lazy='selectin', backref='product', cascade='all, delete')
    user = db.relationship('Users', back_populates='products')

    def __init__(self, name, product_type, original_price, discount_rate,
                 user_id, final_price, status, size, description):
        '''
        initializes the table with data
        '''
        self.name = name
        self.user_id = user_id
        self.product_type = product_type
        self.original_price = original_price
        self.discount_rate = discount_rate
        self.final_price = final_price
        self.status = status
        self.size = size
        self.description = description

class ProductImages(db.Model):
    '''
    stores images related to a certain product
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    filename = db.Column(db.String(100), nullable=False)

    def __init__(self, product_id, filename):
        self.product_id = product_id
        self.filename = filename


class Bookings(db.Model):
    '''
    stores information about tour booking
    '''
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tours.id'), nullable=False)
    tour_name = db.Column(db.String(50), nullable=False)
    amount_paid = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    start_location = db.Column(db.String(50), nullable=False)
    destination = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default='Pending', nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    payment_status = db.Column(db.String(50), default='Pending', nullable=False)
    transaction_id = db.Column(db.String(100))
    reference_code = db.Column(db.String(100), unique=True, nullable=False)
    booking_date = db.Column(db.DateTime, default=datetime.utcnow)
    tour = db.relationship('Tours', back_populates='bookings')
    user = db.relationship('Users', back_populates='bookings')
