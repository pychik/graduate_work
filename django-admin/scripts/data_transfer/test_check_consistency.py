import os

from db_psycopg import get_cursor, pg_get_connection
from db_sqlite import sqlite_get_connection
from dotenv import load_dotenv


load_dotenv()


class ConsistencyChecker:
    """Класс для проверки консистентности данных"""

    def __init__(self, conn_sqlite, conn_pg):
        self.conn_sqlite = conn_sqlite
        self.conn_pg = conn_pg

    def test_row_counts_equals(self, table_name):
        """Тест проверки количества строк в двух бд"""
        rows_count_sqlite = self.get_data_from_table(self.conn_sqlite,
                                                     table,
                                                     only_count_rows=True)
        table_name_with_schema = f'content.{table_name}'
        rows_count_pg = self.get_data_from_table(self.conn_pg,
                                                 table_name_with_schema,
                                                 only_count_rows=True)
        assert rows_count_sqlite == rows_count_pg, 'Количество строк разное!'
        print(f'Количество строк в таблице {table_name} совпадает!')

    def test_data_equals(self, table_name):
        """Тест проверки данных"""

        data_sqlite = self.get_data_from_table(self.conn_sqlite,
                                               table_name,
                                               only_count_rows=False)
        table_name_with_schema = f'content.{table_name}'
        data_postgres = self.get_data_from_table(self.conn_pg,
                                                 table_name_with_schema,
                                                 only_count_rows=False)

        # Т.к. мы могли бы не переносить поля создания и изменения,
        # а проставлять например now()? уберем их из проверки
        skip_check_for_fields = ['created', 'created_at',
                                 'updated_at', 'modified']
        for element in data_sqlite:
            for field in skip_check_for_fields:
                if field in element.keys():
                    element.pop(field)

        for element in data_postgres:
            for field in skip_check_for_fields:
                if field in element.keys():
                    element.pop(field)
        assert data_sqlite == data_postgres
        print(f'Данные в таблице {table_name} совпадают!')

    @staticmethod
    def get_data_from_table(connection, table_name, only_count_rows):

        to_select = '*'

        if only_count_rows:
            to_select = 'count(*)'
        with get_cursor(connection) as cursor:
            sql = f'select {to_select} from {table_name}'
            cursor.execute(sql)

            if only_count_rows:
                row_count = cursor.fetchone()[0]
                return row_count
            sql_data = cursor.fetchall()

        data = [dict(row) for row in sql_data]

        return data

    def get_tables_names(self):
        """Метод для получения всех названий таблиц в бд"""

        with get_cursor(self.conn_sqlite) as cursor:
            sql = 'SELECT name FROM sqlite_master WHERE type="table"'
            cursor.execute(sql)

            table_names = [row['name'] for row in cursor.fetchall()]
        return table_names


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('DB_NAME'),
           'user': os.environ.get('DB_USER'),
           'password': os.environ.get('DB_PASSWORD'),
           'host': os.environ.get('DB_HOST'),
           'port': os.environ.get('DB_PORT')}
    with sqlite_get_connection('db.sqlite') as sqlite_conn,\
            pg_get_connection(dsl) as pg_conn:
        checker = ConsistencyChecker(sqlite_conn, pg_conn)
        tables = checker.get_tables_names()
        for table in tables:
            checker.test_row_counts_equals(table)
            checker.test_data_equals(table)
