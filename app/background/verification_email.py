from flask import url_for, jsonify, render_template
from app.celery import make_celery
from app import create_app, mail
from flask_mail import Message
from app.models import Users
from sqlalchemy.orm import selectinload

app = create_app()

celery = make_celery(app)

@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def send_verification_email(self, user_id):
    '''
    sends verification emails to users
    '''
    try:
        user = Users.query.options(selectinload(Users.profile)).filter_by(id=user_id).first()
        if not user:
            return {'error': 'User not found!'}

        token = user.email_verification_token()
        verification_url = url_for('verify.verify_email', token=token, _external=True)

        msg = Message(
                subject='Verify your email',
                recipients=[user.email],
                sender=app.config['DEFAULT_MAIL_SENDER']
                )
        msg.body = f'Click the following link to verify your email address {verification_url}'
        msg.html = render_template('verification_email.html', user=user, verification_url=verification_url)
        mail.send(msg)
        return {'success': 'Email sent successfully!'}
    except Exception as e:
        self.retry(exc=e)
        return {'error': 'An unexpected error occured. Please try again!'}
