import os


class Config(object):
    postgres_user = os.getenv('POSTGRES_USER')
    postgres_password = os.getenv('POSTGRES_PASSWORD')
    postgres_db = os.getenv('POSTGRES_DB')
    database_url = (
        f'postgresql://{postgres_user}:{postgres_password}@db:5432/{postgres_db}'
    )

    API_KEY = os.getenv('API_KEY', '5e37270a')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', database_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False