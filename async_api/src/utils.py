import logging
import time
from functools import wraps

from core.config import PROJECT_NAME


logger = logging.getLogger(PROJECT_NAME)


def backoff(
        start_sleep_time=0.1,
        factor=2,
        border_sleep_time=20,
        logger_inst=logger,
        max_count_attempts=10
):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка.
    Использует наивный экспоненциальный рост времени повтора(factor)
    до граничного времени ожидания(border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param logger_inst: инстанс логгера
    :param max_count_attempts: максимальное количество попыток
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            current_sleep_time = start_sleep_time
            func_name = func.__name__
            attempt = 1
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_count_attempts:
                        raise e
                    if current_sleep_time < border_sleep_time:
                        current_sleep_time *= 2 ** factor
                    if current_sleep_time >= border_sleep_time:
                        current_sleep_time = border_sleep_time

                    logger_inst.error(f'Error while attempting to call {func_name}: {e}.'
                                      f' Retrying in {current_sleep_time} sec.')
                    time.sleep(current_sleep_time)
                    attempt += 1

        return inner

    return func_wrapper
