import os

from dotenv import load_dotenv


load_dotenv()


class AppConfig:
    postgres_dsl = {'dbname': os.environ.get('POSTGRES_DB'),
                    'user': os.environ.get('POSTGRES_USER'),
                    'password': os.environ.get('POSTGRES_PASSWORD'),
                    'host': os.environ.get('DB_HOST'),
                    'port': os.environ.get('DB_PORT')}
    elastic_dsl = {'scheme': 'http',
                   'host': os.getenv('ETL_HOST', 'elastic'),
                   'port': int(os.getenv('ETL_PORT', 9200))}
