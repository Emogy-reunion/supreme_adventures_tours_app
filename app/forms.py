from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, ValidationError, FloatField, IntegerField, TextAreaField, MultipleFileField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, InputRequired, NumberRange, ValidationError

class RegistrationForm(FlaskForm):
    '''
    validates data from the registration form
    '''
    first_name = StringField('First name', validators=[
        DataRequired(),
        Length(min=2, max=30, message='First name must be between 2 and 30 characters!')])
    last_name = StringField('Last name', validators=[
        DataRequired(),
        Length(min=2, max=30, message='Last name must be between 2 and 30 characters!')])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=4, max=45, message='Email must be between 4 and 45 characters!')])
    username = StringField('Username', validators=[
        DataRequired(message="Username is required"),
        Length(min=3, max=25, message="Username must be between 3 and 25 characters!"),
        Regexp(r'^\w+$', message="Username must contain only letters, numbers, or underscores!")])
    phone_number = StringField('Phone number', validators=[
        DataRequired(),
        Regexp(r'^\+2547\d{8}$', message="Phone number must start with +2547 followed by 8 digits!")
        ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long!"),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter!"),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter!"),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character!")])
    confirmpassword = PasswordField('Confirm password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match!')])

class LoginForm(FlaskForm):
    '''
    validates data from the login form
    '''
    identifier = StringField('Email/Username', validators=[
        DataRequired(),
        Length(min=2, max=50, message='Must be between two and 50 characters!')])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=2, max=50, message='Password ust be between two and 50 characters!')])

class EmailForm(FlaskForm):
    '''
    validates the email
    '''
    email = StringField('Email', validators=[
        DataRequired(),
        Email()])

class PasswordForm(FlaskForm):
    '''
    validates the passwords after an update
    '''
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message="Password must be at least 8 characters long!"),
        Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter!"),
        Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter!"),
        Regexp(r'(?=.*\W)', message="Password must contain at least one special character!")])
    confirmpassword = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match!')
        ])


def custom_length_check(form, field):
    length = len(field.data or '')

    if length < 150:
        raise ValidationError('Description is too short. Minimum 150 characters required.')
    
    if length > 1500:
        raise ValidationError('Description is too long. Maximum 1500 characters allowed.')

class ToursUploadForm(FlaskForm):
    '''
    validates the tours upload details
    '''
    name = StringField('Name', validators=[
        InputRequired(),
        Length(min=5, max=49, message='Name must be between 5 and 49 characters!')
        ])
    start_location = StringField('Start location', validators=[
        InputRequired(),
        Length(min=5, max=49, message='Start location must be between 2 and 49 characters!')
        ])
    destination = StringField('Destination', validators=[
        InputRequired(),
        Length(min=5, max=49, message='Start location must be between 2 and 49 characters!')
        ])
    description = TextAreaField('Description', validators=[
        InputRequired(),
        custom_length_check
        ])
    start_date = DateTimeField('Start date', validators=[
        DataRequired()
        ])
    end_date = DateTimeField('End date', validators=[
        DataRequired()
        ])
    days = IntegerField('Days', validators=[
        DataRequired(),
        NumberRange(min=0)])
    ])
    nights = IntegerField('Nights', validators=[
        DataRequired(),
        NumberRange(min=0)])
    ])
    original_price = FloatField('Original price', validators=[
        DataRequired(),
        NumberRange(min=0)])
    ])
    discount_percent = FloatField('Discount', validators=[
        DataRequired(),
        NumberRange(min=0, max=100)])
        ])
    status = StringField('Status', validators=[DataRequired()])
    included = TextAreaField('Includes', validators=[
        InputRequired(),
        custom_length_check
        ])
    excluded = TextAreaField('Excludes', validators=[
        InputRequired(),
        custom_length_check
        ])
    files = MultipleFileField('Files', validators=[
        InputRequired()
        ])


class ProductsUploadForm(FlaskForm):
	'''
    validates the upload details for the form
    '''
    name = StringField('Sneaker name', validators=[
        DataRequired(),
        Length(min=4, max=45, message='Sneaker name must be betwwen 4 and 45 characters!')])
    original_price = FloatField('Original price', validators=[
        DataRequired(),
        NumberRange(min=0)])
	product_type = StringField('Product type', validators=[DataRequired()])
    discount_rate = FloatField('Discount rate', validators=[
        DataRequired(),
        NumberRange(min=0, max=100)])
    description = TextField('Description', validators=[DataRequired(),
		custom_length_check])
    status = StringField('Status', validators=[DataRequired()])
    size = StringField('Size', validators=[DataRequired()])
    images = MultipleFileField('Images', validators=[DataRequired()])


class UpdateTourForm(FlaskForm):
    '''
    validates the fields when updating a tour
    '''
    name = StringField('Tour name', validators=[
        Optional()
        ])
    start_location = StringField('Start location', validators=[
        Optional()
        ])
    destination = StringField('Destination', validators=[
        Optional()
        ])
    start_date = DateTime('Start date', validators=[
        Optional()
        ])
    end_date = DateTime('End date', validators=[
        Optional()
        ])
    days = IntegerField('Days', validators=[
        Optional()
        ])
    nights = IntegerField('Nights', validators=[
        Optional()
        ])
    original_price = FloatField('Original price', validators=[
        Optional()
        ])
    discount_percent = FloatField('Discount percent', validators=[
        Optional()
        ])
    status = StringField('Status', validators=[
        Optional()
        ])
    included = TextAreaField('Includes', validators=[
        Optional(),
        custom_length_check
        ])
    excluded = TextAreaField('Excludes', validators=[
        Optional(),
        custom_length_check
        ])
