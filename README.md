# Проектная работа 9 спринта
<p align="left">
    <a href="https://www.python.org/" target="blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://docs.docker.com/" target="blank">
        <img alt="Docker" src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
    </a>
</p>

Ссылка на репозиторий - https://github.com/warrinot/notifications_sprint_1

Требования
===

- Python 3.9+
- FastAPI 0.61+

Установка
===

### Docker installation
1. Установить [docker](https://docs.docker.com/engine/installation/)
2. Настройка параметров в файле `.env`
3. Выполнить команду `docker-compose up`
4. Адрес документации API:
   * Swagger - `http://localhost:8000/swagger/`
   * Коллекция для postman: [Link](/notification/swagger_collection.json)

### Built With

* [Gunicorn](https://docs.gunicorn.org/en/stable/) - WSGI HTTP Server for UNIX.
* [Psycopg2-binary](https://www.psycopg.org/) - PostgreSQL database adapter for Python -- C optimisation distribution.

Команда разработчиков
===
* [Черняков Игорь](https://github.com/pychik)
* [Петрушков Станислав](https://github.com/warrinot)
* [Виталий Софронюк](https://github.com/Gilions)


Notifications_Service
===

* Реализовано на Django + Celery + Rabbitmq(как брокер для Celery)
* Сервис уведомлений по сути получает необходимые данные 
от других сервисов и реализизует подготовку шаблонов
и отправку данных пользователям
* При получении данных через API создается notification_log с необходимыми данными и типом
* Задача в celery(task_discover_new) подхватывает новые notification_log'и 
и отправляет их в обработку в задачу task_process_log
* В этой задаче выбирается обработчик по типу уведомления, подготавливаются данные и отправляются через SendGridClient
* Так же реализована отправка из админки
