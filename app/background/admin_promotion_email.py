from flask import render_template
from app.celery import make_celery
from app import create_app, mail
from app.models import Users
from datetime import datetime


app = create_app()
celery = make_celery(app)


@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def send_admin_promotion_email(self, email):
    '''
    sends an email to tell users they have been promoted to an admin
    '''
    try:
        current_year =  datetime.now().year
        user = Users.query.filter_by(email=email).first()

        if not user or user.role != 'admin':
            return {'error': 'User no longer exists or is not an admin. Email not sent.'}

        msg = Message(
                subject='Admin promotion',
                sender=app.config['DEFAULT_MAIL_SENDER'],
                recipients=[email]
                )
        msg.body = (
                f"Hi {user.profile.first_name},\n\n"
                "We’re excited to let you know that your role has been updated to 'Admin' on East Monarch.\n"
                "You can now access admin features such as managing tours, merchandise, and other users.\n\n"
                "If you were not expecting this change, please contact support immediately.\n\n"
                "Thank you,\n"
                "Supreme Adventures Team"
                                                                              )
        msg.html = render_template('admin_promotion.html', user=user, current_year=current_year)
        mail.send(msg)
        return {'success': 'Email sent successfully!'}
    except Exception as e:
        self.retry(exc=e)
        return {'error': 'Email not sent because of an unexpected error!'}
