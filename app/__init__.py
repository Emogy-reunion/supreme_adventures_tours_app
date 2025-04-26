from flask import Flask
from config import  Config

def create_app():
    '''
    initializes the app
    returns the app instance
    '''
    app = Flask(__name__)
    app.from_object(Config)
    return app
