from config.celery import TaskQueue, app


@app.task(bind=True, queue=TaskQueue.QUEUE_DEFAULT)
def task_test(self):
    print(f'================{self.__name__}===========')
