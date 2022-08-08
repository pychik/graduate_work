# Сравниваем базы данных ClickHouse и MongoDB
[![ClickHouse](https://img.shields.io/badge/-ClickHouse-464646?style=flat-square&logo=ClickHouse)](https://clickhouse.com/)
[![mongodb](https://img.shields.io/badge/-mongodb-464646?style=flat-square&logo=mongodb)](https://www.mongodb.com/)
[![python](https://img.shields.io/badge/-python-464646?style=flat-square&logo=python)](https://www.python.org/)


![2608907282](https://user-images.githubusercontent.com/68146917/182671381-acfa90bc-3734-4dc8-847f-5219f0f99310.jpeg)

Требования
===

- Python 3.9+
- Docker-compose

Цель
===

В данной работе будет производится скорость записи и считывания двух баз данных. Сравнивать NoSQL базу данных с реляционной БД, смысла не было, при больших объемах данных, скорость поиска и записи информации в реляционных БД значительно снижается. В нашем случаи требуется база данных, которая может обрабатывать большие объемы данных, при этом сохраняя высокую скорость, как чтения так и записи. Дополнительным условиям является возможность масштабирования.

ClickHouse, а так же MongoDB используются для хранения и обработки больших объемов данных. Данные базы отлично масштабируются, обладают гибкими настройками.

*Примечание:* Тестирование проводилось на базовых настройках баз данных.

В данном тестировании будут произведены следующие действия:
- Запись 200 000 строк.
- Запись 500 000 строк.
- Чтение полной таблицы, 200 000 и 500 000 строк.
- Чтения фильтрованной информации.
- Агрегирование данных.

Результат тестирования:
| Actions            	| ClickHouse     	| MongoDB        	|
|--------------------	|----------------	|----------------	|
| write 200k         	| 0:00:06.752818 	| 0:00:02.801940 	|
| write ~ 500k       	| 0:00:16.352666 	| 0:00:05.418817 	|
| read all 200k      	| 0:00:00.801502 	| 0:00:02.077103 	|
| read all ~ 500k    	| 0:00:01.873989 	| 0:00:03.639679 	|
| read slice ~ 60k   	| 0:00:00.237163 	| 0:00:00.507474 	|
| read slice ~ 110k  	| 0:00:00.304750 	| 0:00:00.930982 	|
| read avg movies    	| 0:00:00.304750 	| 0:00:00.134037 	|
| read avg bookmarks 	| 0:00:00.019882 	| 0:00:00.185994 	|

Как видно из результатов тестирования, MongoDB производит запись значительно быстрее ClickHouse, но в тот же момент ClickHouse немного быстрее MongoDB при чтении данных. Важно отметить, чтение у двух баз данных очень быстрое.

Что касается выбора базы данных для нашего проекта, мы будем использовать MongoDB.

Выбор пал по следующим причинам:
- Высокая скорость записи данных, мы будем использовать базу данных без Kafka.
- Высокая скорость чтения данных.
- Отличная возможность масштабирования.
- База данных гибко настраивается.
- Позволяет хранить и обрабатывать больший объемы данных.
- Хорошая документация.
- Возможность асинхронной записи и чтения данных.

Что касается ClickHouse, данная база данных была создана для хранения большого количества статистических данных, ClickHouse отличное решения для проектов использующих BigData. Высока скорость чтения и колонкоориентированность позволяют выполнять сложные аналитические запросы быстрее чем у MongoDB. В случаи с нашем проектом, данные будут изменятся, для этих целей ClickHouse к сожалению не подойдет.

Установка
===

### Docker
1. Установить [docker](https://docs.docker.com/engine/installation/), если он не установлен.
2. Выполните команду `cp .env.dist .env`
3. Собираем проект, команда `docker-compose build`
4. Запускаем проект, команда `docker-compose up benchmark`