from typing import List

from models import Movie


class DataTransformer:

    def __init__(self, data: List[Movie], index_name: str):
        self.data = data
        self.index_name = index_name

    def transform_data(self) -> List[dict]:

        def transform_item(item: Movie) -> dict:
            transformed_item = {
                '_id': item.uuid,
                '_index': self.index_name,
                **item.dict(),
                'director': item.director,
            }
            return transformed_item

        transformed_data = list(map(transform_item, self.data))
        return transformed_data
