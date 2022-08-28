import logging

from config import settings
from jinja2 import Environment
from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from models import DataModel, UserData


class SendgridSender:
    def __init__(self, data: DataModel):
        self._data = data

    @property
    def data(self):
        return self._data

    def _send(self, address: str, subject: str, data: str):
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=address,
            subject=subject,
            plain_text_content=data)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API)
            response = sg.send(message)

        except HTTPError:
            logging.exception('Error send email')
        else:
            if response.status_code != 202:
                logging.error(f'Error send email, {response}')

    def _create_srs(self, template, user_info) -> str:
        user_context = user_info.dict()

        env = Environment(autoescape=True)
        template_obj = env.from_string(template)
        return template_obj.render(**user_context)

    def execute(self):
        for user_info in self.data.user_list:
            letter = self._create_srs(self.data.template, user_info)
            self._send(user_info.email, user_info.subject, letter)

        logging.info(f'Handled {len(self.data.user_list)} notifications')