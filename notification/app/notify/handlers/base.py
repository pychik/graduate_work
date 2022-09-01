from notify.models import NotificationLog, NotificationTypes, NotificationStages


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
        pass
