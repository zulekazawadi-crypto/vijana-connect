import base64
from datetime import datetime

import requests
from django.conf import settings


class MpesaError(Exception):
    """Raised when something goes wrong while talking to Safaricom."""


def format_phone(phone):
    """Turn 0712345678, +254712345678 or 712345678 into 254712345678 (the format Daraja needs)."""
    digits = ''.join(ch for ch in str(phone) if ch.isdigit())

    if digits.startswith('0') and len(digits) == 10:
        digits = '254' + digits[1:]
    elif len(digits) == 9 and digits[0] in '71':
        digits = '254' + digits

    if digits.startswith('254') and len(digits) == 12:
        return digits
    raise MpesaError('Enter a valid Safaricom number, for example 0712345678.')


def get_access_token():
    """OAuth step: swap our consumer key and secret for a temporary access token."""
    if not settings.MPESA_CONSUMER_KEY or not settings.MPESA_CONSUMER_SECRET:
        raise MpesaError('M-Pesa is not set up yet. Add the keys to the .env file.')

    url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    try:
        response = requests.get(
            url,
            auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET),
            timeout=30,
        )
        response.raise_for_status()
        return response.json()['access_token']
    except (requests.RequestException, KeyError, ValueError) as error:
        raise MpesaError(f'Could not get an access token from Safaricom: {error}')


def stk_push(phone, amount, account_reference, description):
    """Ask Safaricom to show the M-Pesa PIN prompt on the customer's phone."""
    if not settings.MPESA_PASSKEY or not settings.MPESA_CALLBACK_URL:
        raise MpesaError('M-Pesa is not set up yet. Add the passkey and callback URL to the .env file.')

    token = get_access_token()

    # The password is the shortcode + passkey + timestamp, encoded in base64
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()
    ).decode()

    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': int(amount),
        'PartyA': phone,                              # the customer paying
        'PartyB': settings.MPESA_SHORTCODE,           # the business receiving
        'PhoneNumber': phone,                         # the phone that gets the prompt
        'CallBackURL': settings.MPESA_CALLBACK_URL,   # where Safaricom sends the result
        'AccountReference': account_reference[:12],
        'TransactionDesc': description[:13],
    }

    try:
        response = requests.post(
            f"{settings.MPESA_BASE_URL}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers={'Authorization': f'Bearer {token}'},
            timeout=30,
        )
        data = response.json()
    except (requests.RequestException, ValueError) as error:
        raise MpesaError(f'Could not reach Safaricom: {error}')

    # ResponseCode "0" means Safaricom accepted the request
    if data.get('ResponseCode') != '0':
        message = data.get('errorMessage') or data.get('ResponseDescription') or 'Safaricom refused the request.'
        raise MpesaError(message)

    return data