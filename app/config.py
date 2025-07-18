'''
stores the application's configuration settings
'''
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

class Config():
    ENV = 'development'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_COOKIE_SAMESITE = 'Lax'
    CELERY_BROKER_URL = os.getenv("BROKER_URL")
    CELERY_BACKEND_URL = os.getenv('BACKEND_URL')
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    FRONTEND_URL = os.getenv('FRONTEND_URL')
    SERVER_NAME = 'localhost:5000'  # Enables _external URLs in background tasks
    PREFERRED_URL_SCHEME = 'http'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    DEFAULT_MAIL_SENDER = os.getenv('DEFAULT_MAIL_SENDER')
    WTF_CSRF_ENABLED = False
    CONSUMER_KEY= os.getenv('CONSUMER_KEY')
    CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
    PASSKEY = os.getenv('PASSKEY')
    SHORT_CODE = os.getenv('SHORT_CODE')
    MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL')
