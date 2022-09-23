import logging
import secrets
import string
import time
from datetime import datetime
from functools import wraps
from http.client import BAD_REQUEST, UNPROCESSABLE_ENTITY

from flask_restx import abort
from marshmallow import ValidationError
from settings.config import PROJECT_NAME
from user_agents import parse


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


def generate_password():
    # Генерируем временный пароль
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(20))
    return password


def create_new_user(data: dict):
    # Создаем нового пользователя
    from models import Role, User
    from schemas.users import UserSchema
    from settings.datastore import security

    try:
        validated_data = UserSchema().load(data)
        user = User.create(**validated_data)
        role = Role.get_by_name('user')
        user.add_role(role, security)
        return user
    except ValidationError as err:
        abort(UNPROCESSABLE_ENTITY, errors=err.messages)
    except Exception as err:
        logger.error(err)
        abort(BAD_REQUEST, errors='Не удалось создать нового юзера, попробуйте еще раз')


def create_or_update_user_service(data: dict):
    # Регистрируем либо обновляем OAuth сервис пользователя.
    from models import UserOauthServices
    user_service = UserOauthServices.query.filter_by(
        user_id=data.get('user_id'), service=data.get('service')
    ).first()
    if not user_service:
        UserOauthServices.create(**data)
    else:
        data = {key: data[key] for key in data if key not in {'user_id', 'service'}}
        data.update(dict(updated_at=datetime.utcnow()))
        user_service.update(**data)


def get_user_device_type(ua_string: str):
    user_agent = parse(ua_string)
    if user_agent.is_mobile:
        user_device_type = 'mobile'
    elif user_agent.is_tablet:
        user_device_type = 'smart'
    else:
        user_device_type = 'web'
    return user_device_type
