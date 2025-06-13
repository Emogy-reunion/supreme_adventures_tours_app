from flask import Flask
from .config import Config
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_mail import Mail
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
mail = Mail()

def create_app():
    '''
    initializes the app
    returns the app instance
    '''
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'uploads')

    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    return app
