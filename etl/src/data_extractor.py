import datetime
from typing import Generator, List, Tuple
from uuid import UUID

from db_psycopg import PostgresConnection
from dotenv import load_dotenv
from state import State
from utils import backoff


load_dotenv()


class DataExtractor:
    batch_size = 100
    modified_field = 'modified'

    def __init__(self, state: State, dsl: dict):
        self.state = state
        self.connection = PostgresConnection(dsl)

    @backoff()
    def _make_query(self, sql: str, params: List, many=False) -> Generator:
        cursor = self.connection.get_cursor()
        with cursor as cur:
            cur.execute(sql, params)
            if many:
                while True:
                    rows = cur.fetchmany(self.batch_size)
                    if not rows:
                        break
                    yield rows
            else:
                rows = cur.fetchall()
                yield rows

    def get_modified_ids(self, table_name: str, since: datetime.datetime) -> tuple:
        sql = f'''
                SELECT id
                FROM content.{table_name}
                WHERE modified > %s
                ORDER BY modified
               '''
        params = [since]

        rows = self._make_query(sql, params, many=True)
        all_ids = list()
        for batch in rows:
            all_ids.extend([row[0] for row in batch])

        return tuple(all_ids)

    def get_filmwork_ids(self, ids: Tuple[UUID], joined_table: str) -> tuple:
        sql = f'''
            SELECT DISTINCT fw.id, fw.modified
            FROM content.film_work fw
            LEFT JOIN content.{joined_table}_film_work jfw ON jfw.film_work_id = fw.id
            WHERE jfw.{joined_table}_id IN %s
            ORDER BY fw.modified
              '''
        params = [ids]
        rows = self._make_query(sql, params, many=True)
        all_ids = list()
        for batch in rows:
            all_ids.extend([row[0] for row in batch])
        return tuple(all_ids)

    def get_filmworks_data(self, filmwork_ids: Tuple[UUID]) -> List:
        if not filmwork_ids:
            return []

        sql = '''
                SELECT
                    fw.id AS uuid,
                    fw.rating AS imdb_rating,
                    array_agg(DISTINCT g.name) AS genre,
                    fw.title AS title,
                    fw.description AS description,
                    array_agg(DISTINCT p.full_name)
                           FILTER(WHERE pfw.role = 'director') AS director,
                    array_agg(DISTINCT p.full_name)
                           FILTER(WHERE pfw.role = 'actor') AS actors_names,
                    array_agg(DISTINCT p.full_name)
                           FILTER(WHERE pfw.role = 'writer') AS writers_names,
                    json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                           FILTER(WHERE pfw.role = 'actor') AS actors,
                    json_agg(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name))
                           FILTER(WHERE pfw.role = 'writer') AS writers
                FROM
                    content.film_work fw
                LEFT JOIN content.person_film_work pfw ON
                    pfw.film_work_id = fw.id
                LEFT JOIN content.person p ON
                    p.id = pfw.person_id
                LEFT JOIN content.genre_film_work gfw ON
                    gfw.film_work_id = fw.id
                LEFT JOIN content.genre g ON
                    g.id = gfw.genre_id
                WHERE
                    fw.id IN %s
                GROUP BY
                    fw.id
                ORDER BY fw.modified;
        '''
        params = [filmwork_ids]
        data = self._make_query(sql, params)
        film_data = list()
        for batch in data:
            film_data.extend([dict(row) for row in batch])
        return film_data
