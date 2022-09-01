from .base import BaseHandler
from notify.models import NotificationStages
from notify.utility.email_sender import get_mail_client
from notify.dataclasses import DataModel, UserData
from notify.utils import get_rendered_template


class WelcomeHandler(BaseHandler):
    template_name = 'welcome_letter.html'
    subject = 'Welcome letter'

    def __init__(self, nl):
        super().__init__(nl)


    def send(self):

        data_to_send = self.prepare_data()

        mail_client = get_mail_client(data_to_send)

        try:
            response = mail_client.execute()
            self.nl.log_success(response)
        except Exception as e:
            self.nl.log_error(e)
        else:
            self.nl.change_stage(NotificationStages.success, save=False)
        finally:
            self.nl.send_tries += 1
            self.nl.save()

    def prepare_data(self):
        data = self.nl.notification_data

        user_list = [UserData(**data)]

        values = dict(username=data.get('first_name'))
        template = get_rendered_template(self.template_name, values).encode('utf-8')
        subject = self.subject

        data_to_send = dict(user_list=user_list,
                            template=template,
                            subject=subject)

        try:
            return DataModel(**data_to_send)
        except Exception as e:
            raise e
