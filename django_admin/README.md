# Проектное задание: Docker-compose

Приступим к улучшению сервиса в области DevOps. Настройте запуск всех компонентов системы (Django, Nginx и Postgresql) с использованием docker-compose.

**Требования к работе:**

- Напишите dockerfile для Django.
- Для настройки Nginx можно пользоваться наработками из этой темы, но ревьюеры будут обязательно запускать ваше решение, поэтому убедитесь, что всё работает правильно.
- Уберите версию Nginx из заголовков. Версии любого ПО лучше всегда скрывать от посторонних глаз, чтобы вашу админку случайно не взломали. Найдите необходимую настройку в официальной документации и проверьте, что она работает корректно. Убедиться в этом можно с помощью «Инструментов разработчика» в браузере.
- Отдавайте статические файлы Django через Nginx, чтобы не нагружать сервис дополнительными запросами: перепишите `location` таким образом, чтобы запросы на `/admin` шли без поиска статического контента. То есть, минуя директиву `try_files $uri $uri/ @backend;`.

**Подсказки и советы:**

- Этого урока должно быть достаточно для понимания принципов конфигурирования. Если у вас появятся какие-то вопросы по параметрам, ищите ответы [в официальной документации](https://nginx.org/ru/).
- Для выполнения задачи про `/admin` нужно посмотреть порядок поиска `location`.
- Для работы со статикой нужно подумать, как залить данные в файловую систему контейнера с Nginx.
- Для задания дана базовая структура, которой можно пользоваться.