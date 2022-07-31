import os
import sqlite3

from db_psycopg import pg_get_connection
from db_sqlite import sqlite_get_connection
from dotenv import load_dotenv
from pg_saver import PostgresSaver
from psycopg2.extensions import connection as _connection
from sqlite_loader import SQLiteLoader


load_dotenv()

BATCH_SIZE = 500


def load_from_sqlite(connection: sqlite3.Connection, pg_connect: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""

    postgres_saver = PostgresSaver(pg_connect)
    sqlite_loader = SQLiteLoader(connection)

    tables = ['genre', 'person', 'film_work', 'genre_film_work', 'person_film_work']

    for table in tables:
        data_gen = sqlite_loader.load_table_gen(table, batch_size=BATCH_SIZE)
        postgres_saver.save_all_data(data_gen, table)


if __name__ == '__main__':
    dsl = {'dbname': os.environ.get('POSTGRES_DB'),
           'user': os.environ.get('POSTGRES_USER'),
           'password': os.environ.get('POSTGRES_PASSWORD'),
           'host': os.environ.get('DB_HOST'),
           'port': os.environ.get('DB_PORT')}
    with sqlite_get_connection('db.sqlite') as sqlite_conn, \
            pg_get_connection(dsl) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
