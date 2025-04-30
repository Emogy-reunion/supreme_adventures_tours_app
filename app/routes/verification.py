from flask import Blueprint, redirect, url_for, current_app
from app.models import Users, db


verify = Blueprint('verify', __name__)

@verify.route('/verify_email/<token>', methods=['POST'])
def verify_email(token):
    '''
    verifies the email by verifying the token
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
