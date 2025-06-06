from app import create_app()
import requests
from requests.auth import HTTPBasicAuth


app = create_app()


def get_access_token():
    consumer_key = app.config['CONSUMER_KEY']
    consumer_secret = app.config['CONSUMER_SECRET']
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    token = response.json().get('access_token')
    return token
