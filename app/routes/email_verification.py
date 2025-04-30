from flask import Blueprint, redirect, current_app, jsonify
from app.models import Users, db
from app.forms import ResendVerificationEmailForm
from app.background.verification_email import send_verification_email


verify = Blueprint('verify', __name__)

@verify.route('/verify_email/<token>', methods=['POST'])
def verify_email(token):
    '''
    verifies the email by verifying the token
    on success the user is redirected to a success page
    on failure the user is redirected to a failure page
    '''
    user = Users.verify_token(token)
    if user:
        try:
            user.verified = True
            db.session.commit()
            return redirect(f'{current_app.config['FRONTEND_URL']}/success_page')
        except Exception as e:
            db.session.rollback()
            return redirect(f'{current_app.config['FRONTEND_URL']}/failure_page')
    else:
        return redirect(f'{current_app.config['FRONTEND_URL']}/failure_page')


@verify.route('/resend_verification_email', methods=['POST'])
def resend_verification_email():
    '''
    resends the user a verification email if verification has failed
    '''
    form = ResendVerificationEmailForm(data=request.get_json())

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    email = form.email.data
    try:
        user = Users.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": 'There is no account associated with this email. Please try again!'}), 404
        send_verification_email.delay(user.id)
        return jsonify({"success": 'We’re sending you a verification email — it should arrive shortly. Please check your email inbox!'}), 200
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500
