import json

from django.conf import settings
from django.test import Client

from home.models import Payment

payment = Payment.objects.filter(status='pending').first()

if payment is None:
    print("No pending payment found. Make one on the Pay page first.")
else:
    # This is the same shape of message Safaricom sends. ResultCode 0 means "paid".
    body = {"Body": {"stkCallback": {
        "MerchantRequestID": payment.merchant_request_id,
        "CheckoutRequestID": payment.checkout_request_id,
        "ResultCode": 0,
        "ResultDesc": "The service request is processed successfully.",
        "CallbackMetadata": {"Item": [
            {"Name": "Amount", "Value": float(payment.amount)},
            {"Name": "MpesaReceiptNumber", "Value": "TEST123ABC"},
            {"Name": "TransactionDate", "Value": 20261120101500},
            {"Name": "PhoneNumber", "Value": int(payment.phone)},
        ]},
    }}}

    url = f"/payments/callback/{settings.MPESA_CALLBACK_SECRET}/"
    response = Client(HTTP_HOST='127.0.0.1').post(
        url, data=json.dumps(body), content_type='application/json'
    )
    print("Server answered:", response.status_code, response.content.decode())