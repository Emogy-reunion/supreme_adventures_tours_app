from flask import Blueprint, request, jsonify
from models import Users, Profile

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    '''
    registers the user to the database
    '''
    form = RegistrationForm(data=request.form)

    if not form.validate():
        return jsonify({"errors": form.errors})

    first_name = form.first_name.data
    last_name = form.last_name.data
    email = form.email.data
    username = form.username.data
    phone_number = form.phone_number.data

    try:
        user_exists = Users.query.filter(Users.email == email | Users.username == Username).first()
        if user_exists:
            return jsonify({'error': 'A user with this email or username already exists. Please try logging in or use a different email.'}), 409

        user = Users(email=email, username=username, phone_number=phone_number, password=password)
        db.session.add(user)
        db.session.flush()
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
