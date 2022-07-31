import sqlite3
from contextlib import contextmanager


@contextmanager
def sqlite_get_connection(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
    finally:
        conn.close()
