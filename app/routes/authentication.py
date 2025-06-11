from flask import Blueprint, request, jsonify
from app import db
from app.models import Users, Profiles
from app.forms import RegistrationForm, LoginForm
from app.background.verification_email import send_verification_email
from flask_jwt_extended import set_refresh_cookies, set_access_cookies, get_jwt_identity, jwt_required, unset_jwt_cookies, create_access_token, create_refresh_token
from sqlalchemy import or_

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    registers the user to the database
    '''
    form = RegistrationForm(data=request.get_json())

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    first_name = form.first_name.data.lower()
    last_name = form.last_name.data.lower()
    email = form.email.data.lower()
    username = form.username.data.lower()
    phone_number = form.phone_number.data
    password = form.password.data

    try:
        user_exists = Users.query.filter(or_(Users.email == email, Users.username == username)).first()
        if user_exists:
            return jsonify({'error': 'A user with this email or username already exists. Please try logging in or use a different email.'}), 409

        user = Users(email=email, username=username, phone_number=phone_number, password=password)
        db.session.add(user)
        db.session.flush()

        profile = Profiles(user_id=user.id, first_name=first_name, last_name=last_name)
        db.session.add(profile)
        db.session.commit()
        send_verification_email.delay(user.id)
        user_data = {
                'role': user.role,
                'success': 'Your account has been created. We’re sending you a verification email — it should arrive shortly!'
                }
        return jsonify(user_data), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

@auth.route('/login', methods=['POST'])
def login():
    '''
    authenticates the user
    '''
    form = LoginForm(data=request.get_json())

    if not form.validate():
        return jsonify({"error": form.errors}), 400

    identifier = form.identifier.data.lower()
    password = form.password.data

    try:
        user = None
        if '@' in identifier:
            user = Users.query.filter_by(email=identifier).first()
        else:
            user = Users.query.filter_by(username=identifier).first()

        if user and user.check_password(password):
            '''
            checks if the user exists
            checks if the passwords match
            logins in the user if both the above exist
            '''
            access_token = create_access_token(identity=str(user.id))
            refresh_token = create_refresh_token(identity=str(user.id))

            response = jsonify({
                'role': user.role,
                'success': 'Logged in successfully'})
            set_access_cookies(response, access_token)
            set_refresh_cookies(response, refresh_token)
            return response, 200
        else:
            return jsonify({"error": 'Invalid login credentials. Please try again!'}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    '''
    logs the user out by destroying the jwt cookies
    '''
    try:
        response = jsonify({"success": 'Successfully logged out!'})
        unset_jwt_cookies(response)
        return response, 200
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500

@auth.route('/refresh_token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    '''
    create an access token after it expires
    '''
    try:
        user_id = get_jwt_identity()
        response = jsonify({"success": 'Access token refreshed successfully!'})
        set_access_cookies(response, access_token)
        return response, 200
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500
