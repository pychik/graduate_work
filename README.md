# Проектная работа 8 спринта
<p align="left">
    <a href="https://www.python.org/" target="blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://flask.palletsprojects.com/en/2.1.x/" target="blank">
        <img src="https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white"/>
    </a>
    <a href="https://redis.io/" target="blank">
        <img src="https://img.shields.io/badge/redis-%23DD0031.svg?&style=for-the-badge&logo=redis&logoColor=white"/>
    </a>
    <a href="https://docs.docker.com/" target="blank">
        <img alt="Docker" src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
    </a>
</p>

Ссылка на репозиторий - [ugc_sprint_1](https://github.com/Gilions/ugc_sprint_1)

Проектные работы в этом модуле выполняются в командах по 3 человека. Процесс обучения аналогичен сервису, где вы изучали асинхронное программирование. Роли в команде и отправка работы на ревью не меняются.

Распределение по командам подготовит команда сопровождения. Куратор поделится с вами списками в Slack в канале #group_projects.

Задания на спринт вы найдёте внутри тем.


Требования
===

- Python 3.9+
- FastAPI 0.61+

Установка
===

### Docker installation
1. Установить [docker](https://docs.docker.com/engine/installation/)
2. Настройка параметров в файле `.env`
3. Выполнить команду `docker-compose up` или `make build`
4. Адрес документации API:
   * Swagger - `http://localhost/api/v1/`
5. По умолчанию будет создана учетная запись администратора:
    * Логин - admin@admin.ru
    * Пароль - admin
6. По умолчанию будут созданы роли:
    * admin
    * manager
    * user

### Built With

* [Gunicorn](https://docs.gunicorn.org/en/stable/) - WSGI HTTP Server for UNIX.
* [Gevent](http://www.gevent.org/) - Coroutine-based network library.
* [Psycopg2-binary](https://www.psycopg.org/) - PostgreSQL database adapter for Python -- C optimisation distribution.
* [Flask](https://fastapi.tiangolo.com/) - web framework for building APIs.
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) - Adds SQLAlchemy support to your Flask application.
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) - SQLAlchemy database migrations for Flask applications using Alembic..
* [Flask-Security](https://flask-security.readthedocs.io/en/3.0.0/) - Simple security for Flask apps..
* [Flask-Marshmallow](https://flask-marshmallow.readthedocs.io/en/latest/) - Flask + marshmallow for beautiful APIs.
* [Flask-Restx](https://flask-restx.readthedocs.io/en/latest/) - Fully featured framework for fast, easy and documented API development with Flask.
* [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/) - Extended JWT integration with Flask.

#### Дополнительные репозитории
* [Auth_sprint_1](https://github.com/TimBerk/Auth_sprint_1) - Cервис авторизации с системой ролей.

### Make команды

* **up** - запуск сервера разработки.
* **stop** - остановка сервера разработки.
* **build** - сборка сервера разработки.

Команда разработчиков
===
* [Черняков Игорь](https://github.com/pychik)
* [Алексей Комиссаров](https://github.com/akomissarov2020)
* [Петрушков Станислав](https://github.com/warrinot)
* [Виталий Софронюк](https://github.com/Gilions)

Kafka_Api
===
*  запуск в отладочном режиме c confluent из папки ugc 
  - "docker-compose up -f docker-compose-debug.yaml"
  - и в соседнем терминале "uvicorn main:app --reload"
*  запуск в нормальном режиме из папки ugc 
  - "docker-compose up"

