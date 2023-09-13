import os
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotification

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
                "return_url": "http://localhost:8000/participate/"
            },
            "capture": True,
            "description": "Тестовое описание оплаты",
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

    return payment

    # {
    #     'type': 'notification',
    #     'event': 'payment.succeeded',
    #     'object': {
    #         'id': '2c938420-000f-5000-9000-17e16a87f815',
    #         'status': 'succeeded',
    #         'amount': {
    #             'value': '500.00',
    #             'currency': 'RUB'
    #         },
    #         'income_amount': {
    #             'value': '482.50',
    #             'currency': 'RUB'
    #         },
    #         'description': 'Тестовое описание оплаты',
    #         'recipient': {
    #             'account_id': '251745',
    #             'gateway_id': '2119240'
    #         },
    #         'payment_method': {
    #             'type': 'bank_card',
    #             'id': '2c938420-000f-5000-9000-17e16a87f815',
    #             'saved': False,
    #             'title': 'Bank card *4444',
    #             'card': {
    #                 'first6': '555555',
    #                 'last4': '4444',
    #                 'expiry_year': '2023',
    #                 'expiry_month': '11',
    #                 'card_type': 'MasterCard',
    #                 'issuer_country': 'US'
    #             }
    #         },
    #         'captured_at': '2023-09-13T08:18:54.213Z',
    #         'created_at': '2023-09-13T08:18:40.756Z',
    #         'test': True,
    #         'refunded_amount': {
    #             'value': '0.00',
    #             'currency': 'RUB'
    #         },
    #         'paid': True,
    #         'refundable': True,
    #         'metadata': {
    #             'karathon_id': '8',
    #             'participant_id': '2'
    #         },
    #         'authorization_details': {
    #             'rrn': '264868140061133',
    #             'auth_code': '731330',
    #             'three_d_secure': {
    #                 'applied': False,
    #                 'method_completed': False,
    #                 'challenge_completed': False
    #             }
    #         }
    #     }
    # }
