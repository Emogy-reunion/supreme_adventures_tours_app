from flask import render_template
from app.celery import make_celery
from app import create_app, mail
from app.models import Users
from datetime import datetime

app = create_app()
celery = make_celery(app)


@celery.task(bind=True, max_retries=3, default_retry_delay=10)
def send_admin_revoke_email(self, email):
    '''
    sends an email to notify user that their admin privileges have been revoked
    '''
    try:
        current_year = datetime.now().year
        user = Users.query.filter_by(email=email).first()

        if not user or user.role == 'admin':
            return {'error': 'User no longer exists or still has admin privileges!'}

        msg = Message(
                subject='Admin Privilege revocation',
                sender=app.config['DEFAULT_MAIL_SENDER'],
                recipients=[email]
                )
        msg.body=(
                 f"Hi {user.profile.first_name},\n\n"
                 "We wanted to inform you that your admin privileges on East Monarch have been revoked. "
                 "You no longer have access to administrative features such as managing tours, merchandise, or user accounts.\n\n"
                 "If you believe this was a mistake or have any questions, please contact support immediately.\n\n"
                 "Thank you,\n"
                 "Supreme Adventures Team"
                )
        msg.html = render_template('admin_revoke.html', user=user, current_year=current_year)
        mail.send(msg)
        return {'success': 'Email sent successfully!'}
    except Exception as e:
        self.retry(exc=e)
        return {'error': 'An unexpected error occurred. Email not sent!'}

