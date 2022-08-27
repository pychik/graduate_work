from config.celery import app
from config.celery import TaskQueue


@app.task(bind=True, queue=TaskQueue.QUEUE_DEFAULT)
def task_test(self):
    print(f'================{self.__name__}===========')
