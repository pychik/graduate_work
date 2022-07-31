from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor


class PostgresConnection:

    def __init__(self, credentials: dict):
        self.credentials = credentials

    @contextmanager
    def _pg_get_connection(self):
        con = psycopg2.connect(**self.credentials, cursor_factory=DictCursor)
        try:
            yield con
        finally:
            con.close()

    @contextmanager
    def get_cursor(self):
        connection = self._pg_get_connection()
        with connection as conn:
            cur = conn.cursor()
            try:
                yield cur
            finally:
                cur.close()
