from flask import Blueprint, request, jsonify
from app import db
from app.forms import EmailForm, PasswordForm
from app.models import Users
from app.background.password_reset_email import send_password_reset_email

reset = Blueprint('reset', __name__)

@reset.route('/reset_password', methods=['POST'])
def reset_password():
    '''
    allows user to reset their password
    fetches the user email
    uses it to send a password reset link
    '''
    form = EmailForm(data=request.get_json())

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    email = form.email.data.lower()

    try:
        user = Users.query.filter_by(email=email).first()

        if user and user.verified:
            send_password_reset_email.delay(user.id)
        return jsonify({"success": "If the email is registered and verified, a password reset link will be sent."}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500


@reset.route('/update_password', methods=['PATCH'])
def update_password():
    '''
    saves the new password to the database
    '''
    try:
        form = PasswordForm(data=request.get_json())
        token = request.json.get('token')
    
        if not form.validate():
            return jsonify({"errors": form.errors}), 400

        password = form.password.data

        user = Users.verify_token(token)

        if user:
            user.password_hash = user.generate_passwordhash(password)
            db.session.commit()
            return jsonify({"success": 'Password updated successfully!'}), 200
        else:
            return jsonify({"error": "Password reset failed. Please ensure the user details are correct."}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
