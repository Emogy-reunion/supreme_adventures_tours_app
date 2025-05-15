from flask import url_for, jsonify, render_template
from app.celery import make_celery
from app import create_app
from flask_mail import Mail, Message
from app.models import Users, db

app = create_app()

celery = make_celery(app)
mail = Mail(app)

@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def send_verification_email(self, user_id):
    '''
    sends verification emails to users
    '''
    try:
        user = db.session.get(Users, user_id)
        if not user:
            return {'error': 'User not found!'}

        token = user.email_verification_token()
        verification_url = url_for('verify.verify_email', token=token, _external=True)

        msg = Message(
                subject='Verify your email',
                recipients=[user.email],
                sender='emogyreunion@gmail.com'
                )
        msg.body = f'Click the following link to verify your email address {verification_url}'
        msg.html = render_template('verification_email.html', user=user, verification_url=verification_url)
    except Exception as e:
        self.retry(exc=e, max_retries=3, countdown=10)
        return {'error': 'An unexpected error occured. Please try again!'}
