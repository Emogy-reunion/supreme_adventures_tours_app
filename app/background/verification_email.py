from app.celery import make_celery
from app import create_app

app = create_app()

celery = make_celery(app)

@celery.task
def send_verification_email(user):
    '''
    sends verification emails to users
    '''

