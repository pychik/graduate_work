import functools
from notify.handlers.base import HANDLERS_MAP
from notify.models import NotificationLog


def get_handler(nl: NotificationLog):
    return HANDLERS_MAP.get(nl.type)(nl)


def close_connection_if_not_usable(connection):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
            was_closed = False
    except Exception:
        connection.close()
        was_closed = True

    return was_closed


def unlock_log(notification_guid):
    from django.db import connection
    close_connection_if_not_usable(connection)

    nl = NotificationLog.get_object(guid=notification_guid)
    nl.locked = False
    nl.save(update_fields=['locked'])


def unlock_log_finally(func):
    @functools.wraps(func)
    def wrapper(guid, **kwargs):
        was_exception_raised = False
        try:
            func(guid, **kwargs)
        except Exception:
            was_exception_raised = True
            raise
        finally:
            if was_exception_raised:
                unlock_log(guid)
    return wrapper
