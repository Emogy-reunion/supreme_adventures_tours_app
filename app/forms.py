from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

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
        Regexp('^\w+$', message="Username must contain only letters, numbers, or underscores!")])
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
