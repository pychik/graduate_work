import json
from yookassa import Configuration, Payment, Refund
from graduate_work.core import settings
from .interface import BillingInterface


class YookassaBilling(BillingInterface):
    """
    Class for operate with YooKassa sdk
    """
    account_id = settings.YOOKASSA_ID
    secret_key = settings.YOOKASSA_API_SECRET
    redirect_url = settings.REDIRECT_URL

    def __init__(self, description, subscribe_type_id, user_id, value):
        self._subscribe_type_id = subscribe_type_id
        self._user_id = user_id
        self._value = value
        self._description = description

    @property
    def description(self):
        return self._description

    @property
    def value(self):
        return self._value

    @property
    def user_id(self):
        return self._user_id

    @property
    def subscribe_type_id(self):
        return self.subscribe_type_id

    def create_payment(self) -> dict:
        """Create and process payment via Yookassa agregator"""

        Configuration.account_id = self.account_id
        Configuration.secret_key = self.secret_key
        _payment = Payment.create({
                            "amount": {
                                "value": self.value,
                                "currency": "RUB"
                            },
                            "payment_method_data": {
                                "type": "bank_card"
                            },
                            "confirmation": {
                                "type": "redirect",
                                "return_url": self.redirect_url
                            },
                            "capture": True,
                            "description": self.description,
                            "save_payment_method": True

                            })

        """в ответе 
            {
              "id": "2419a771-000f-5000-9000-1edaf29243f2",
              "status": "pending",
              "paid": false,
              "amount": {
                "value": "100.00",
                "currency": "RUB"
              },
              "confirmation": {
                "type": "redirect",
                "confirmation_url": "https://yoomoney.ru/api-pages/v2/payment-confirm/epl?orderId=2419a771-000f-5000-9000-1edaf29243f2"
              },
              "created_at": "2019-03-12T11:10:41.802Z",
              "description": "Заказ №37",
              "metadata": {
                "order_id": "37"
              },
              "recipient": {
                "account_id": "100500",
                "gateway_id": "100700"
              },
              "refundable": false,
              "test": false
            }"""

        # Отсюда мы вытаскиваем payment id и извне сохраняем вместе с description в бд?
        return json.loads(_payment.json())


    @staticmethod
    def auto_payment(value: str, description: str, success_payment_id: str = None, ):
        """
        Auto payment logic
        """
        # Если мы получили запрос на автоплатеж (допустим мы это делаем сразу с оплатой подписки)
        # нам надо передать Yookassa такую форму чтоб получить success payment_ id  и в дальнейшем его использовать
        # Yookassa получит подтверждение пользователя на авто
        if not success_payment_id:
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
                    "return_url": settings.REDIRECT_URL
                },
                "capture": True,
                "description": description,
                "save_payment_method": True
            })
            """возвращается 
                {
                  "id": "22e18a2f-000f-5000-a000-1db6312b7767",
                  "status": "succeeded",
                  "paid": true,
                  "amount": {
                    "value": "2.00",
                    "currency": "RUB"
                  },
                  "authorization_details": {
                    "rrn": "10000000000",
                    "auth_code": "000000",
                    "three_d_secure": {
                      "applied": true
                    }
                  },
                  "captured_at": "2018-07-18T17:20:50.825Z",
                  "created_at": "2018-07-18T17:18:39.345Z",
                  "description": "Заказ №72",
                  "metadata": {},
                  "payment_method": {
                    "type": "bank_card",
                    "id": "22e18a2f-000f-5000-a000-1db6312b7767",
                    "saved": true,
                    "card": {
                      "first6": "555555",
                      "last4": "4444",
                      "expiry_month": "07",
                      "expiry_year": "2022",
                      "card_type": "MasterCard",
                      "issuer_country": "RU",
                      "issuer_name": "Sberbank"
                    },
                    "title": "Bank card *4444"
                  },
                  "refundable": true,
                  "refunded_amount": {
                    "value": "0.00",
                    "currency": "RUB"
                  },
                  "recipient": {
                    "account_id": "100500",
                    "gateway_id": "100700"
                  },
                  "test": false
                }"""
            # отсюда забираем payment_method.id  это и есть наш success_method_id
        else:
            # Если наш автоворкер пришел то он переда success_payment_id  и сработало это условие
            # подтверждене пользователя в этом случае не нужно
            _payment = Payment.create({
                "amount": {
                    "value": "2.00",
                    "currency": "RUB"
                },
                "capture": True,
                "payment_method_id": success_payment_id,
                "description": description
            })
        return json.loads(_payment.json())

    @staticmethod
    def refund_payment(value: str, payment_id: str):
        """
        Refund logic
        """
        _refund = Refund.create({
            "amount": {
                "value": value,  # "2.00"
                "currency": "RUB"
            },
            "payment_id": payment_id  # "21740069-000f-50be-b000-0486ffbf45b0"
        })
        return json.loads(_refund.json())





