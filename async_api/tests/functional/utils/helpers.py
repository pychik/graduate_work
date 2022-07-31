from typing import List


async def create_index_to_es(es_client, index, body=None):
    if not es_client.indices.exists(index=index):
        es_client.indices.create(index, body=body)


async def load_data_to_es(es_client, index, test_data):
    bulk_create = []
    for obj in test_data:
        bulk_create.append({'index': {'_index': index, '_id': obj['uuid']}})
        bulk_create.append(obj)
    es_client.bulk(body=bulk_create, doc_type='_doc', refresh=True)


async def remove_data_from_es(es_client, index, test_data):
    bulk_delete = []
    for obj in test_data:
        bulk_delete.append({
            'delete': {
                '_index': index, '_id': obj['uuid'],
            }
        })
    es_client.bulk(body=bulk_delete)


async def remove_data_from_redis(redis_client, prefix):
    for key in redis_client.scan_iter(f'{prefix}*'):
        redis_client.delete(key)


def transform_movies_data(movies_data: List) -> List:
    """Преобразует данные из фикстуры для эластика в данные ответа API"""
    transformed_data = [{'uuid': movie['uuid'],
                         'title': movie['title'],
                         'imdb_rating': movie['imdb_rating']}
                        for movie in movies_data]
    return transformed_data


def transform_persons_data(persons_data: List) -> List:
    """Преобразует данные из фикстуры для эластика в данные ответа API"""
    transformed_data = [{'uuid': person['uuid'],
                         'full_name': person['full_name']}
                        for person in persons_data]
    return transformed_data


def transform_genre_data(genre_data: List) -> List:
    """Преобразует данные из фикстуры для эластика в данные ответа API"""
    transformed_data = [{
        'uuid': genre['uuid'],
        'name': genre['name']}
        for genre in genre_data]
    return transformed_data


def transform_films_search(fims_data: List, search: str) -> List:
    """Преобразует данные из фикстуры для эластика в данные ответа API"""
    transformed_data = [{
        'uuid': film['uuid'],
        'title': film['title'],
        'imdb_rating': film['imdb_rating']}
        for film in fims_data if search in film['title']]
    return transformed_data
