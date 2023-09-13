import os
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification

from apps.account.models import Participant

Configuration.configure(os.environ.get("YOOKASSA_TEST_ID"), os.environ.get("YOOKASSA_TEST_KEY"))


@staticmethod
def create_payment(karathon, participant):
    payment = Payment.create(
        {
            "amount": {
                "value": "500.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "https://karathon.yuriyzhidkov.ru/participate/"
            },
            "capture": True,
            "description": "Оплата участия в {number} карафоне".format(number=karathon.number),
            "metadata": {
                'karathon_id': karathon.id,
                'participant_id': participant.id
            },
            "receipt": {
                "customer": {
                    "full_name": '{last_name} {first_name} {middle_name}'.format(last_name=participant.last_name,
                                                                                 first_name=participant.first_name,
                                                                                 middle_name=participant.middle_name),
                    "email": participant.email,
                    "phone": participant.phone,
                },
                "items": [
                    {
                        "description": "Запись участника на карафон",
                        "quantity": "1.00",
                        "amount": {
                            "value": "500.00",
                            "currency": "RUB"
                        },
                        "vat_code": "1",
                    }
                ]
            }
        }
    )

    return payment


@staticmethod
def confirmation_payment(payment_data):
    notification_object = WebhookNotification(payment_data)
    payment = notification_object.object

    if payment.status == 'succeeded':
        karathon_id = payment.metadata['karathon_id']
        participant_id = payment.metadata['participant_id']
        Participant.objects.get(id=participant_id).karathon.add(karathon_id)
