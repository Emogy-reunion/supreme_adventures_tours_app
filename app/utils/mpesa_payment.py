from app import create_app()
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime


app = create_app()


def get_access_token():
    consumer_key = app.config['CONSUMER_KEY']
    consumer_secret = app.config['CONSUMER_SECRET']
    url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    token = response.json().get('access_token')
    return token


def generate_password():
    shortcode = app.config['SHORT_CODE']
    passkey = app.config['PASSKEY']

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + passkey + timestamp
    encoded_string = base64.b64encode(data.to_encode.encode())
    return encoded_string.decode('utf-8')
