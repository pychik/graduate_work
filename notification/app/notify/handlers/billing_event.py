from notify.dataclasses import DataModel, UserData
from notify.utils import get_rendered_template

from .base import BaseHandler


# TODO create general class with notification type checker
class BillingPaymentHandler(BaseHandler):
    template_name = 'billing_payment_status.html'
    subject = 'Yandex payment status'

    def prepare_data(self):
        data = self.nl.notification_data

        user_list = [UserData(**data)]
        payment_status = data.get('message')
        values = dict(first_name=data.get('first_name'), payment_status=payment_status)
        template = get_rendered_template(self.template_name, values)
        subject = self.subject

        data_to_send = dict(user_list=user_list,
                            template=template,
                            subject=subject)

        try:
            return [DataModel(**data_to_send)]
        except Exception as e:
            self.nl.log_error(e)
            self.fail()


class BillingSubsExpiresHandler(BaseHandler):
    template_name = 'billing_subscription_expires.html'
    subject = 'Yandex Films Subscription Expires'

    def prepare_data(self):
        data = self.nl.notification_data

        user_list = [UserData(**data)]
        subscription_type = data.get('message')
        values = dict(first_name=data.get('first_name'), subscription_type=subscription_type)
        template = get_rendered_template(self.template_name, values)
        subject = self.subject

        data_to_send = dict(user_list=user_list,
                            template=template,
                            subject=subject)

        try:
            return [DataModel(**data_to_send)]
        except Exception as e:
            self.nl.log_error(e)
            self.fail()


class BillingAutoPaymentHandler(BaseHandler):
    template_name = 'billing_auto_payment.html'
    subject = 'Yandex Films Subscription Expires'

    def prepare_data(self):
        data = self.nl.notification_data

        user_list = [UserData(**data)]
        subscription_type = data.get('message')
        values = dict(first_name=data.get('first_name'), subscription_type=subscription_type)
        template = get_rendered_template(self.template_name, values)
        subject = self.subject

        data_to_send = dict(user_list=user_list,
                            template=template,
                            subject=subject)

        try:
            return [DataModel(**data_to_send)]
        except Exception as e:
            self.nl.log_error(e)
            self.fail()
