from flask import Blueprint, request, jsonify
from models import Users, Profiles, db
from forms import RegistrationForm
from app.background.verification_email import send_verification_email

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    registers the user to the database
    '''
    form = RegistrationForm(data=request.form)

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    username = form.username.data
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
        return jsonify({'success': 'Your account has been created. We’re sending you a verification email — it should arrive shortly!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
