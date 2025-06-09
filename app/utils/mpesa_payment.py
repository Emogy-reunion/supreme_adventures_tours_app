from app import create_app
import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
import random


app = create_app()


def generate_reference_code():
    today = datetime.now().strftime('%Y%m%d')
    rand_part = random.randint(1000, 9999)
    return f"BK-{today}-{rand_part}"


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

def send_stk_push(amount, phone_number, reference_code, tour_name):
    token = get_access_token()
    password = generate_password()

    headers = {
            'Authorization': "Bearer "+ token,
            'Content-Type': 'application/json'
            }

    payload = {
            'BusinessShortCode': app.config['SHORT_CODE'],
            'Password': password,
            'Timestamp': timestamp,
            'TransactionType': 'CustomerBuyGoodsOnline',
            'Amount': amount,
            'PartyA': phone_number,
            'PartyB': app.config['SHORT_CODE'],
            'PhoneNumber': phone_number,
            'CallBackUrl': app.config['MPESA_CALLBACK_URL'],
            'AccountReference': reference_code,
            'TransactionDesc': f"Payment for {tour_name}"
            }
    url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
