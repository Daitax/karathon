import os
from yookassa import Configuration, Payment

Configuration.configure(os.environ.get("YOOKASSA_TEST_ID"), os.environ.get("YOOKASSA_TEST_KEY"))


def send_yookassa_request(karathon, participant):
    payment = create_payment(karathon, participant)

    print(payment)
    print(payment.confirmation.confirmation_url)

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
