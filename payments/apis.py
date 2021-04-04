import json

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from PaysafeTest.settings import PAYSAFE_PRIVATE_KEY


@csrf_exempt
def process_payment(request, amount, token):
    val = {
        "merchantRefNum": "1559900597607",
        "amount": int(amount),
        "currencyCode": "USD",
        "dupCheck": True,
        "settleWithAuth": False,
        "paymentHandleToken": token,
        "customerIp": "10.10.12.64",
        "description": "Paysafe subscription"
    }

    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Basic ' + PAYSAFE_PRIVATE_KEY,
        'Simulator': '\'EXTERNAL\''
    }

    url = 'https://api.test.paysafe.com/paymenthub/v1/payments'

    req = requests.post(url, json=val, headers=headers)
    print(req.text)

    resp_status = req.json().get('status') or ''

    if resp_status == 'COMPLETED':
        response_success = {
            'success': True
        }

    else:
        response_success = {
            'success': True
        }

    return HttpResponse(json.dumps(response_success, indent=4), content_type='application/json')
    # return HttpResponse(data=response_success, status=status.HTTP_200_OK)
