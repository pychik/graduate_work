from notify.handlers.welcome import WelcomeHandler
from notify.models import NotificationTypes, NotificationLog
from notify.handlers.base import BaseHandler


HANDLERS_MAP = {
    NotificationTypes.like: BaseHandler,
    NotificationTypes.welcome: WelcomeHandler,
}


def get_handler(nl: NotificationLog):
    return HANDLERS_MAP.get(nl.notification_type)(nl)