import uuid

import requests
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.conf import settings
import json
import simplejson


MERCHANT_ID = settings.MERCHANT_ID
PAY_SECRET_KEY = settings.PAY_SECRET_KEY

BASE_URL = settings.BASE_URL
CALLBACK_BASE_URL = settings.CALLBACK_BASE_URL


def get_url(user_data=None, course=None, discount_price=None) -> str:
    if discount_price:
        price = simplejson.dumps(discount_price)
    else:
        price = simplejson.dumps(user_data.package_membership.price)
    data = {
        "order": f"{user_data.id}",
        "amount": price,
        "currency": "KGS",
        "description": f'{user_data}',
        "language": "ru",
        # "payment_system": payment_system,
        "options": {
            "callbacks": {
                "result_url": CALLBACK_BASE_URL + "/api/v1/purchases/payment_response/",
                "check_url": CALLBACK_BASE_URL,
                "cancel_url": CALLBACK_BASE_URL,
                # "success_url": CALLBACK_BASE_URL + f"/user/checkout/?status=success&order={user_data.id}",
                # "failure_url": CALLBACK_BASE_URL + f"/user/checkout/?status=error&order={user_data.id}",
                "success_url": CALLBACK_BASE_URL,
                "failure_url": CALLBACK_BASE_URL,
                "back_url": CALLBACK_BASE_URL,
                "capture_url": CALLBACK_BASE_URL
            }
        }
    }
    response = requests.post(BASE_URL + "v4/payments",
                             json=data,
                             auth=(MERCHANT_ID, PAY_SECRET_KEY),
                             headers={'X-Idempotency-Key': f'{user_data.id}'}
                             )
    if response.status_code != status.HTTP_201_CREATED:
        raise ValidationError({"message": "Ошибка при запросе PayBox"})
    data = json.loads(response.content)
    if not course:
        user_data.payment_url = user_data.payment_url if user_data.payment_url else data['payment_page_url']
        user_data.payment_id = user_data.payment_id if user_data.payment_id else data.get('id', None)
        user_data.paid_price = price
        user_data.type = user_data.package_membership.get_type_display()
        user_data.save()
    return data


def get_payment_info(payment_id: str) -> dict:
    response = requests.get(BASE_URL + f"v4/payments/{payment_id}",
                            auth=('534869', 'PewoawvojgOjlbtV'),
                            headers={'X-Idempotency-Key': f'{str(uuid.uuid4())}'}
                            )
    if response.status_code != status.HTTP_200_OK:
        raise ValidationError({"message": "Ошибка при запросе PayBox " + str(response.status_code)})

    data = json.loads(response.content)

    return data


def cancel_payment(purchase):
    response = requests.post(BASE_URL + f"payments/{purchase.payment_id}/cancel",
                             json={},
                             auth=('534869', 'PewoawvojgOjlbtV'),
                             headers={'X-Idempotency-Key': f'{purchase.uuid}'}
                             )
    data = json.loads(response.content)

    return data.get('code', None)
