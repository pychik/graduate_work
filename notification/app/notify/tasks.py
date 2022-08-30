import logging

from celery_once import QueueOnce
from config.celery import TaskQueue, app
from notify.models import NotificationLog
from notify.utils import unlock_log_finally
from notify.handlers.router import get_handler


@app.task(bind=True, queue=TaskQueue.QUEUE_DEFAULT)
def task_test(self):
    print(f'================{self.__name__}===========')


logger = logging.getLogger(__name__)


@app.task(base=QueueOnce, queue=TaskQueue.QUEUE_DEFAULT)
@unlock_log_finally
def task_process_log(guid):

    nl = NotificationLog.get_object(guid)

    handler = get_handler(nl)
    handler.process()
    return 'Processed'


@app.task(queue=TaskQueue.QUEUE_DEFAULT)
def task_discover_new(batch_size=50):

    new_guids = list(NotificationLog.new.values_list('guid', flat=True)[:batch_size])

    NotificationLog.objects.filter(guid__in=new_guids).update(locked=True)

    for guid in new_guids:
        task_process_log.apply_async((guid,))
    return len(new_guids)
