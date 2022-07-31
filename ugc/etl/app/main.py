import logging

from clickhouse import ClickHouseStreamClient


if __name__ == '__main__':
    try:
        ClickHouseStreamClient().process()
        logging.info('ETL сервис, все миграции были выполнены!')
    except Exception as e:
        logging.warning(f'Миграции не были выполнены, возникла ошибка - {e}!')
