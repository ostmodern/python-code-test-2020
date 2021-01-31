import os

database_url = (
    f'sqlite:///'
)

API_KEY = os.getenv('API_KEY', '5e37270a')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', database_url)
SQLALCHEMY_TRACK_MODIFICATIONS = False