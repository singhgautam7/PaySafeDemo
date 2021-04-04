import json

import requests

from PaysafeTest.settings import PAYSAFE_PRIVATE_KEY


class HelperPaySafe:

    @staticmethod
    def create_paysafe_customer_profile(user_instance):
        val = {
            "merchantCustomerId": 'grs-django-paysafe-demo-user' + str(user_instance.id),
            "locale": "en_US",
            "firstName": user_instance.first_name,
            "lastName": user_instance.last_name,
            "dateOfBirth": {
                "year": 1981,
                "month": 10,
                "day": 24
            },
            "email": user_instance.email,
            "phone": "777-444-8888",
            "ip": "192.0.126.111",
            "gender": "M",
            "nationality": "Canadian",
            "cellPhone": "777-555-8888",
            "status": "ACTIVE"
        }

        print(json.dumps(val, indent=4))

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + PAYSAFE_PRIVATE_KEY,
            'Simulator': '\'EXTERNAL\''
        }
        req = requests.post('https://api.test.paysafe.com/paymenthub/v1/customers', json=val, headers=headers)

        print(req.text)

        customer_id = req.json().get('id') or None

        # Save customer id if it is not None
        if customer_id is not None:
            user_instance.profile.paysafe_user_id = customer_id
            user_instance.profile.save()

        return customer_id

    @staticmethod
    def get_paysafe_customer_profile(user_instance):

        # If paysafe id is already saved then get that
        if user_instance.profile.paysafe_user_id != '':
            return user_instance.profile.paysafe_user_id

        merchant_customer_id = 'grs-django-paysafe-demo-user' + str(user_instance.id)
        url = 'https://api.test.paysafe.com/paymenthub/v1/customers?merchantCustomerId=' + merchant_customer_id
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + PAYSAFE_PRIVATE_KEY,
            'Simulator': '\'EXTERNAL\''
        }
        req = requests.get(url, headers=headers)

        print(req.text)
        customer_id = req.json().get('id') or None

        # Save customer id if it is not None
        if customer_id is not None and user_instance.profile.paysafe_user_id == '':
            user_instance.profile.paysafe_user_id = customer_id
            user_instance.profile.save()

        return customer_id

    @staticmethod
    def get_or_create_paysafe_customer_profile(user_instance):
        customer_id = HelperPaySafe.get_paysafe_customer_profile(user_instance)
        if customer_id is None:
            customer_id = HelperPaySafe.create_paysafe_customer_profile(user_instance)
        return customer_id

    @staticmethod
    def get_single_user_customer_token(paysafe_customer_id):
        url = 'https://api.test.paysafe.com/paymenthub/v1/customers/{}/singleusecustomertokens'. \
            format(paysafe_customer_id)

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Basic ' + PAYSAFE_PRIVATE_KEY,
            'Simulator': '\'EXTERNAL\''
        }
        val = {
            "merchantRefNum": "1559900597607",
            "paymentTypes": [
                "CARD"
            ]
        }

        req = requests.post(url, json=val, headers=headers)
        print(req.text)

        return req.json().get('singleUseCustomerToken') or None
