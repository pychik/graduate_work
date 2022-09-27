# Дипломная работа
<p align="left">
    <a href="https://www.python.org/" target="blank">
        <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    </a>
    <a href="https://docs.docker.com/" target="blank">
        <img alt="Docker" src="https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white">
    </a>
</p>

Ссылка на репозиторий - https://github.com/pychik/graduate_work

Требования
===

- Python 3.9+
- Django 0.61+
- Celery 5.0+
- RabbitMq
- Kafka

Установка
===

### Docker installation
1. Установить [docker](https://docs.docker.com/engine/installation/)
2. Настройка параметров в файле `.env` каждого из микросервисов. Для примера -env.dist
3. Выполнить команду `docker-compose up`


Команда разработчиков
===
* [Черняков Игорь](https://github.com/pychik)
* [Петрушков Станислав](https://github.com/warrinot)
* [Виталий Софронюк](https://github.com/Gilions)


Billing_Service
===
Для функциональности Billing cервис связан с микросервисами нашего проекта- Notifications, Auth.
Взаимодействие с сервисами происходит через Kafka. В сервисе используется Celery+RabbitMQ для создания задач по графику

### На данных момент реализованы
* Api routes:
  * Создание новой транзакции оплаты
  * Получение данных о подписках
  * Получение данных по всем платежам пользователя с user_id
  * Получение всех данных по конкретному платежу
  * Создание возврата по транзакции
    * Создан метод перерасчета времени использования подписки и возвращаемой суммы
  * Route для получения статуса платежа от платежной системы
* Обработка событий
  * При изменение статуса в Billing, в топики notification, auth кладется 
    информация для обработки, чтоб уведомить пользователя и сменить его роль
* Частично офромлены тесты

### Доработка
* Тесты
* Сделать обработку задач для Celery, проверка статуса подписок и срока автоплатежей
* Добавить Схему с архитектурой проекта