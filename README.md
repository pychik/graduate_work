# Проектная работа 9 спринта
<p align="left">
    <a href="https://www.python.org/" target="blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://docs.docker.com/" target="blank">
        <img alt="Docker" src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
    </a>
</p>

Ссылка на репозиторий - [ugc_sprint_2](https://github.com/warrinot/notifications_sprint_1)

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
   * Swagger - `http://localhost:8000/swagger/`

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

* Реализовано
  * 
  * ELK + Sentry для всего проекта
  * Произведен анализ хранилищ MongoDb vs Clickhouse (ugc/benchmark) Описание в ugc/benchmark/Readme
  * WorkFlow с отправкой статуса в телеграмм группу разработчиков
 

Запуск Notifications 
  * Первичный запуск
     * chmod +x runner.sh (запустит docker compose и произведет настройку mongo)
  *  Вторичный запуск из папки
     * docker-compose up -d