from notify.handlers.assignment import NewAssignmentHandler
from notify.handlers.base import BaseHandler
from notify.handlers.likes import LikesHandler
from notify.handlers.new_movie import NewMovieHandler
from notify.handlers.welcome import WelcomeHandler
from notify.models import NotificationLog, NotificationTypes


HANDLERS_MAP = {
    NotificationTypes.welcome: WelcomeHandler,
    NotificationTypes.like: LikesHandler,
    NotificationTypes.new_movie: NewMovieHandler,
    NotificationTypes.assignment: NewAssignmentHandler
}


def get_handler(nl: NotificationLog):
    return HANDLERS_MAP.get(nl.notification_type, BaseHandler)(nl)
