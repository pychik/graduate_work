from django.utils import timezone
from notify.models import NotificationLog, NotificationStages
from notify.utility.email_sender import get_mail_client


MAX_SEND_RETRIES = 5


class BaseHandler:

    def __init__(self, nl: NotificationLog):
        self.nl = nl

    def process(self):

        if self.nl.stage == NotificationStages.new:
            self.send()

        if self.nl.stage == NotificationStages.failed:
            if self.nl.send_tries < MAX_SEND_RETRIES:
                self.send()
        # unlock
        self.nl.unlock()

    def send(self):
        data_to_send = self.prepare_data()

        for data in data_to_send:

            mail_client = get_mail_client(data)

            try:
                mail_client.execute()
            except Exception as e:
                self.nl.log_error(e)
            else:
                message = f'Success at {timezone.now()}'
                self.nl.log_success(message)
                self.nl.change_stage(NotificationStages.success, save=False)

            self.nl.send_tries += 1
            self.nl.save()

    def prepare_data(self):
        raise Exception('Not implemented')
