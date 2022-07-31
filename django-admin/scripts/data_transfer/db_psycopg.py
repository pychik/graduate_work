from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor


@contextmanager
def pg_get_connection(connection_param):
    con = psycopg2.connect(**connection_param, cursor_factory=DictCursor)
    try:
        yield con
    finally:
        con.close()


@contextmanager
def get_cursor(connection):
    cur = connection.cursor()
    try:
        yield cur
    finally:
        cur.close()
