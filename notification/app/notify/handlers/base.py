from notify.models import NotificationLog, NotificationTypes


class BaseHandler:

    def __init__(self, nl: NotificationLog):
        self.nl = nl

    def process(self):
        # process
        # process()
        # unlock
        self.nl.unlock()


HANDLERS_MAP = {NotificationTypes.like: BaseHandler}
