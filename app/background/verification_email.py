from flask import url_for, jsonify, render_template
from app.celery import make_celery
from app import create_app
from flask_mail import Mail, Message
from app.models import Users, db

app = create_app()

celery = make_celery(app)
mail = Mail(app)

@celery.task(bind=True, max_retries=3, default_retry_delay=60)
@def send_verification_email(user_id):
    '''
    sends verification emails to users
    '''
    try:
        user = db.session.get(Users, user_id)
        if not users:
            return jsonify({'error': 'User not found!'}), 404

        verification_token = user.email_verification_token()
        verification_url = url_for('/verify_token', verification_token=verification_token, _external=True)

        msg = Message(
                subject='Verify your email',
                recipients=[user.email],
                sender='info.realestateapp@gmail.com'
                )
        msg.body = f'Click the following link to verify your email address {verification_url}'
        msg.html = render_template('verification_email.html', user=user, verification_url=verification_url)
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
