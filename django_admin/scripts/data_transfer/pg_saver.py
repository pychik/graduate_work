from dataclasses import astuple

from db_psycopg import get_cursor
from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values


class PostgresSaver:

    def __init__(self, connection: _connection):
        self.connection = connection

    def save_all_data(self, data_gen, table_name: str, schema='content'):
        """Метод сохранения данных в базу postgres"""

        table_name_with_schema = f'{schema}.{table_name}'

        with get_cursor(self.connection) as cursor:
            for chunk in data_gen:
                fields = chunk[0].__annotations__.keys()
                fields_template = ', '.join(fields)
                fields_template = fields_template.replace('created_at',
                                                          'created')
                fields_template = fields_template.replace('updated_at',
                                                          'modified')

                data = [astuple(element) for element in chunk]

                insert_query = '''INSERT INTO {table} ({fields})
                                  VALUES %s
                                  ON CONFLICT (id) DO NOTHING;''' \
                    .format(table=table_name_with_schema,
                            fields=fields_template)

                execute_values(cursor, insert_query, data)

                self.connection.commit()
