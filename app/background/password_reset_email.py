from flask import url_for, render_template, jsonify
from app.backround.verification_email import mail
from app.models import Users, db
from flask_mail import Message
from app.celery import make_celery
from app import create_app

app = create_app()
celery = make_celery(app)

@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def send_password_reset_email(self, user_id):
    '''
    sends an email that contains a link allowing user to reset password
    '''
    try:
        user = db.session.get(Users, user_id)

        if not user:
            return {'error': 'User not found!'}

        verification_token = user.email_verification_token()
        verification_url = url_for('verify.verify_password_reset_token', verification_token=verification_token, _external=True)
        msg = Message(
                subject='Password reset link',
                sender='info.realestate@gmail.com',
                recipients=[user.email])
        msg.body = f"We have recieved a password reset request, it it was you click the following link to reset your password {verification_url} otherwise ignore it"
        msg.html = render_template('password_reset.html', user=user, verification_url=verification_url)
        return ('success': 'Email sent successfully!'}
    except Exception as e:
        self.retry(exc=e, countdown=10, max_retries=3)
         return {'error': 'An unexpected error occured. Please try again!'}
