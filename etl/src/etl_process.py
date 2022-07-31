import datetime

from config import AppConfig
from data_extractor import DataExtractor
from data_transformer import DataTransformer
from etl_connect import EtlConnect
from loguru import logger
from models import Movie
from state import JsonFileStorage, State


class EtlProcess:
    tables = ['film_work', 'genre', 'person']
    pg_dsl = AppConfig.postgres_dsl
    elastic_dsl = AppConfig.elastic_dsl
    storage = JsonFileStorage('state.json')
    state = State(storage)
    extractor = DataExtractor(state, pg_dsl)
    etl = EtlConnect(elastic_dsl)
    modified_field = 'modified'
    index_name = 'movies'

    def process(self) -> None:
        # для теста будем указывать дату заведомо раннюю чем все изменения
        self.state.set_state(self.modified_field, datetime.datetime.min)

        last_modified = self.state.get_state(self.modified_field)
        if not last_modified:
            last_modified = datetime.datetime.now() - datetime.timedelta(days=1)
        for table in self.tables:
            modified_ids = self.extractor.get_modified_ids(table, last_modified)
            if not modified_ids:
                logger.info(f'No changes in table: {table} yet')
                continue

            if table == 'film_work':
                film_work_ids = modified_ids
            else:
                film_work_ids = self.extractor.get_filmwork_ids(modified_ids, table)

            films_data = self.extractor.get_filmworks_data(film_work_ids)

            movies = [Movie(**film_data) for film_data in films_data]

            final_data = DataTransformer(movies, self.index_name).transform_data()

            self.etl.bulk_insert(final_data)

        self.state.set_state(self.modified_field, datetime.datetime.now())
