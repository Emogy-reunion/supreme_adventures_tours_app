from flask import Flask

def create_app():
    '''
    initializes the app
    returns the app instance
    '''
    app = Flask(__name__)
    return app
