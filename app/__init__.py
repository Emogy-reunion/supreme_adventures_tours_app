from flask import Flask
from .config import Config
from .models import db, bcrypt
from .background.verification_email import mail

def create_app():
    '''
    initializes the app
    returns the app instance
    '''
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    return app
