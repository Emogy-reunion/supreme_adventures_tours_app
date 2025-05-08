from flask import Blueprint, redirect, current_app, jsonify
from app.models import Users, db
from app.forms import EmailForm
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
            return redirect(f"{current_app.config['FRONTEND_URL']}/verification_status/true")
        except Exception as e:
            db.session.rollback()
            return redirect(f"{current_app.config['FRONTEND_URL']}/verification_status/false")
    else:
        return redirect(f"{current_app.config['FRONTEND_URL']}/verification_status/false")


@verify.route('/resend_verification_email', methods=['POST'])
def resend_verification_email():
    '''
    resends the user a verification email if verification has failed
    '''
    form = EmailForm(data=request.get_json())

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    email = form.email.data
    try:
        user = Users.query.filter_by(email=email).first()

        if user and not user.verified:
            send_verification_email.delay(user.id)

        return jsonify({"success": 'If an account with that email exists and is unverified, we are sending a new verification link — it should arrive shortly. Please check your email inbox!'}), 200
    except Exception as e:
        return jsonify({"error": 'An unexpected error occured. Please try again!'}), 500


@verify.route('/verify_reset_password_token/<token>', methods=['POST'])
def verify_reset_password_token(token):
        '''
        verifies the user by verifying the token sent via email
        on success: the user is redirected to a page where they input their new passwords
        on failure: the user is redirected to a failure page
        '''
        try:
            user = Users.verify_token(token)
            if user:
                return redirect(f"{current_app.config['FRONTEND_URL']}/update_password/{user.id}")
            else:
                return redirect(f"{current_app.config['FRONTEND_URL']}/password_failure_page")
            except Exception as e:
                return redirect(f"{current_app.config['FRONTEND_URL']}/password_failure_page")
