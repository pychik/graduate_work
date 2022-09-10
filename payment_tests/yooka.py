import json
from yookassa import Configuration, Payment
from config import Settings
import asyncio

Configuration.account_id = Settings.SHOP_ID
Configuration.secret_key = Settings.SHOP_API_SECRET


def create_payment(value, description):
    _payment = Payment.create({
                            "amount": {
                                "value": value,
                                "currency": "RUB"
                            },
                            "payment_method_data": {
                                "type": "bank_card"
                            },
                            "confirmation": {
                                "type": "redirect",
                                "return_url": Settings.REDIRECT_URL
                            },
                            "capture": True,
                            "description": description
                            })

    return json.loads(_payment.json())


def check_payment(payment_id):
    _payment = json.loads((Payment.find_one(payment_id)).json())
    return _payment
    # while _payment['status'] == 'pending':
    #     _payment = json.loads((Payment.find_one(payment_id)).json())
    #     await asyncio.sleep(3)

    # if _payment['status'] == 'succeeded':
    #     print("SUCCESS RETURN")
    #     print(_payment)
    #     return True
    # else:
    #     print("BAD RETURN")
    #     print(_payment)
    #     return False

p = create_payment(value=100,description="Подпиькопокупошка")
print(p)
c = check_payment(payment_id=p.get("id"))
print(c)