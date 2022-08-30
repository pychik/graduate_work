import logging

from itertools import chain, islice
from python_http_client.exceptions import HTTPError
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, To

from config import settings
from notify import DataModel


class SendgridSender:
    def __init__(self, data: DataModel):
        self._data = data

    @property
    def data(self):
        return self._data

    def _send(self, batch_address: list):
        message = Mail(
            from_email=settings.FROM_EMAIL,
            to_emails=batch_address,
            subject=self.data.subject,
            html_data=self.data.template.body,
            is_multiple=True)
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API)
            response = sg.send(message)

        except HTTPError:
            logging.exception('Error send email')
        else:
            if response.status_code != 202:
                logging.error(f'Error send email, {response}')

    def subs_maker(self, data_model):
        _ddm = {}
        for k, v in dict(data_model).items():
            k = '{{' + k + '}}'
            _ddm[k] = v
        return _ddm

    def _batcher(self):
        to_emails = (To(email=u.email,  # update with your email
                        name=f'{u.first_name}',
                        substitutions=self.subs_maker(u)
                        ) if u.notify == True else None for u in self.data.user_list )
# {
#     '{{name}}': 'Joe',
#     '{{link}}': 'https://github.com/',
#     '{{event}}': 'Developers Anonymous'
# }

        def chunks(iterable, size=1):
            iterator = iter(iterable)
            for first in iterator:
                yield chain([first], islice(iterator, size - 1))
        return chunks(to_emails, settings.BATCH_SIZE)

    def execute(self):
        for batch in self._batcher():
            b = list(batch)
            self._send(batch_address=b)
            logging.info(f'Handled {len(b)} notifications')
