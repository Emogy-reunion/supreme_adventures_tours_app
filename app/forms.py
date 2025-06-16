from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FloatField, IntegerField, TextAreaField, MultipleFileField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, InputRequired, NumberRange, ValidationError, Optional
from app.utils.custom_form_validators import custom_length_check, validate_date_range, validate_price_range, message_length_check

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
        Regexp(r'^254\d{9}$', message='Phone number must start with 254 followed by exactly 9 digits')
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
        DataRequired(),
        Length(min=5, max=49, message='Start location must be between 2 and 49 characters!')
        ])
    description = TextAreaField('Description', validators=[
        InputRequired(),
        custom_length_check
        ])
    start_date = DateTimeField('Start date', format='%Y-%m-%dT%H:%M',validators=[
        DataRequired()
        ])
    end_date = DateTimeField('End date', format='%Y-%m-%dT%H:%M', validators=[
        DataRequired(),
        validate_date_range
        ])
    days = IntegerField('Days', validators=[
        InputRequired(),
        NumberRange(min=1, max=28, message='Days cannot be less than 1 or more than 28')
        ])
    nights = IntegerField('Nights', validators=[
        InputRequired(),
        NumberRange(min=0, max=28, message='Days cannot be less than 0 or more than 28')
        ])
    original_price = FloatField('Original price', validators=[
        DataRequired(),
        NumberRange(min=0, max=10000000)
        ])
    discount_percent = FloatField('Discount', validators=[
        InputRequired(),
        NumberRange(min=0, max=100, message='Discount cannot be less than 0 or more than 100')
        ])
    status = StringField('Status', validators=[
        DataRequired(),
        Length(min=5, max=49, message='Status must be between 2 and 49 characters!')
        ])
    included = TextAreaField('Includes', validators=[
        InputRequired(),
        custom_length_check
        ])
    excluded = TextAreaField('Excludes', validators=[
        InputRequired(),
        custom_length_check
        ])


class ProductsUploadForm(FlaskForm):
    '''
    validates the upload details for the form
    '''
    name = StringField('Product name', validators=[
        DataRequired(),
        Length(min=4, max=45, message='Product name must be betwwen 4 and 45 characters!')])
    original_price = FloatField('Original price', validators=[
        DataRequired(),
        NumberRange(min=0)])
    product_type = StringField('Product type', validators=[
        DataRequired(),
        Length(min=5, max=49, message='Product type must be between 2 and 49 characters!')
        ])
    discount_rate = FloatField('Discount rate', validators=[
        InputRequired(),
        NumberRange(min=0, max=100, message='Discount cannot be less than 0 or more than 100')])
    description = TextAreaField('Description', validators=[
        DataRequired(),
        custom_length_check
        ])
    status = StringField('Status', validators=[
        DataRequired(),
        Length(min=5, max=49, message='Status must be between 2 and 49 characters!')
        ])
    size = StringField('Size', validators=[
        DataRequired(),
        Length(min=1, max=49, message='Size must be between 1 and 49 characters!')
        ])


class UpdateTourForm(FlaskForm):
    '''
    validates the fields when updating a tour
    '''
    name = StringField('Tour name', validators=[
        Optional(),
        Length(min=5, max=49, message='Name must be between 5 and 49 characters!')
        ])
    start_location = StringField('Start location', validators=[
        Optional(),
        Length(min=5, max=49, message='Start location must be between 2 and 49 characters!')
        ])
    destination = StringField('Destination', validators=[
        Optional(),
        ])
    start_date = DateTimeField('Start date', format='%Y-%m-%dT%H:%M', validators=[
        Optional()
        ])
    end_date = DateTimeField('End date', format='%Y-%m-%dT%H:%M', validators=[
        Optional(),
        validate_date_range
        ])
    days = IntegerField('Days', validators=[
        Optional(),
        NumberRange(min=1, max=28, message='Days cannot be less than 1 day or more than 28 nights')
        ])
    nights = IntegerField('Nights', validators=[
        Optional(),
        NumberRange(min=0, max=28, message='Nights cannot be less than 0 or more than 28 nights')
        ])
    original_price = FloatField('Original price', validators=[
        Optional(),
        NumberRange(min=0)
        ])
    discount_percent = FloatField('Discount percent', validators=[
        Optional(),
        NumberRange(min=0, max=100, message='Discount cannot be less than 0 or more than 100')
        ])
    status = StringField('Status', validators=[
        Optional(),
        Length(min=5, max=49, message='Status must be between 2 and 49 characters!')
        ])
    included = TextAreaField('Includes', validators=[
        Optional(),
        custom_length_check
        ])
    excluded = TextAreaField('Excludes', validators=[
        Optional(),
        custom_length_check
        ])
    description = TextAreaField('Description', validators=[
        Optional(),
        custom_length_check
        ])


class UpdateMerchandiseForm(FlaskForm):
    '''
    validates the fields when updating a merchandise
    '''
    name = StringField('Name', validators=[
        Optional(),
        Length(min=4, max=45, message='Product name must be betwwen 4 and 45 characters!')
        ])
    original_price = FloatField('Original price', validators=[
        Optional(),
        NumberRange(min=0)
        ])
    product_type = StringField('Product type', validators=[
        Optional()
        ])
    discount_rate = FloatField('Discount rate', validators=[
        Optional(),
        NumberRange(min=0, max=100)
        ])
    description = TextAreaField('Description', validators=[
        Optional(),
        custom_length_check
        ])
    status = StringField('Status', validators=[
        Optional()
        ])
    size = StringField('Size', validators=[
        Optional()
        ])

class TourSearchForm(FlaskForm):
    '''
    validates the tour search form fields
    '''
    name = StringField('Name', validators=[
        Optional(),
        Length(min=4, max=45, message='Tour name must be betwwen 4 and 45 characters!')])
    destination =  StringField('Name', validators=[
        Optional(),
        Length(min=2, max=45, message='Destination must be betwwen 2 and 45 characters!')])
    start_date = DateTimeField('Start date', format='%Y-%m-%dT%H:%M', validators=[
        Optional(),
        ])
    end_date = DateTimeField('End date', format='%Y-%m-%dT%H:%M', validators=[
        Optional(),
        validate_date_range
        ])
    days = IntegerField('Days', validators=[
        Optional(),
        NumberRange(min=0, message='Days cannot be less than 0!')
        ])
    nights = IntegerField('Nights', validators=[
        Optional(),
        NumberRange(min=0, message='Nights cannot be less than 0!')
        ])
    maximum_price = FloatField('Maximum price', validators=[
        Optional(),
        NumberRange(min=0, message='Maximum price cannot be less than 0!'),
        validate_price_range
        ])
    minimum_price = FloatField('Minimum price', validators=[
        Optional(),
        NumberRange(min=0, message='Minimum cannot be less than 0!')
        ])


class MerchandiseSearchForm(FlaskForm):
    name = StringField('Name', validators=[
        Optional()
        ])
    product_type = StringField('Product type', validators=[
        Optional()
        ])
    size = StringField('Size', validators=[
        Optional()
        ])
    maximum_price = FloatField('Maximum price', validators=[
        Optional(),
        NumberRange(min=0, message='Maximum price cannot be less than 0!'),
        validate_price_range
        ])
    minimum_price = FloatField('Minimum price', validators=[
        Optional(),
        NumberRange(min=0, message='Minimum cannot be less than 0!')
        ])

class PhoneNumberForm(FlaskForm):
    phone_number = StringField('Phone Number', validators=[
        InputRequired(message='Phone number is required'),
        Regexp(r'^254\d{9}$', message='Phone number must start with 254 and contain exactly 12 digits')
        ])

class GuestContactForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(),
        Length(min=2, max=50, message='Name too long! It must be between 2 and 30 characters!')])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(min=4, max=45, message='Email must be between 4 and 45 characters!')])
    message = TextAreaField('Message', validators=[
        InputRequired(),
        message_length_check
        ])


class MemberContactForm(FlaskForm):
    message = TextAreaField('Message', validators=[
        InputRequired(),
        message_length_check
        ])
