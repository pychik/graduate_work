from notify.handlers.base import BaseHandler
from notify.handlers.likes import LikesHandler
from notify.handlers.new_movie import NewMovieHandler
from notify.handlers.welcome import WelcomeHandler
from notify.handlers.birthday import BirthdayHandler
from notify.models import NotificationLog, NotificationTypes


HANDLERS_MAP = {
    NotificationTypes.welcome: WelcomeHandler,
    NotificationTypes.like: LikesHandler,
    NotificationTypes.new_movie: NewMovieHandler,
    NotificationTypes.birthday: BirthdayHandler,
}


def get_handler(nl: NotificationLog):
    return HANDLERS_MAP.get(nl.notification_type, BaseHandler)(nl)
