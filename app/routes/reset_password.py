from flask import Blueprint, request, jsonify
from app.forms import EmailForm
from app.background.password_reset_email import send_password_reset_email

reset = Blueprint('reset', __name__)

@reset.route('/reset_password', methods=['POST'])
def reset_password():
    '''
    allows user to reset their password
    '''
    form = EmailForm(data=request.get_json())

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    email = form.email.data

    try:
        user = Users.query.filter_by(email=email).first()

        if user and user.verified:
            send_password_reset_email.delay(user.id)
        return jsonify({"success": "If the email is registered and verified, a password reset link will be sent."}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
            

