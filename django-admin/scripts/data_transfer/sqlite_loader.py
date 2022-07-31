import sqlite3

from dataclass import DataClassGetter
from db_psycopg import get_cursor


class SQLiteLoader:
    dataclass = None

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection

    def load_table_gen(self, table_name, batch_size):
        """Метод для получения данных из таблицы пачками"""

        self.dataclass = DataClassGetter(table_name).get_dataclass()

        with get_cursor(self.connection) as cursor:

            sql = f'select * from {table_name}'
            cursor.execute(sql)

            while True:
                sql_data = cursor.fetchmany(batch_size)
                if not sql_data:
                    break
                data = [self.dataclass(**row) for row in sql_data]
                yield data

    def get_tables(self):
        """Метод для получения всех названий таблиц в бд"""

        with get_cursor(self.connection) as cursor:

            sql = 'SELECT name FROM sqlite_master WHERE type="table"'
            cursor.execute(sql)

            tables = [row['name'] for row in cursor.fetchall()]
        return tables
