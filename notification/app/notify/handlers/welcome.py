from notify.dataclasses import DataModel, UserData
from notify.models import NotificationStages
from notify.utility.email_sender import get_mail_client
from notify.utils import get_rendered_template
from short_links.utils import create_activation_link

from .base import BaseHandler


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
        user_id = data.get('user_id')
        activation_link = create_activation_link(user_id)
        values = dict(username=data.get('first_name'), activation_link=activation_link)
        template = get_rendered_template(self.template_name, values).encode('utf-8')
        subject = self.subject

        data_to_send = dict(user_list=user_list,
                            template=template,
                            subject=subject)

        try:
            return DataModel(**data_to_send)
        except Exception as e:
            raise e
