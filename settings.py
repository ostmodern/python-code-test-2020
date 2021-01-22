import os

# GLOBAL
TEST = os.environ.get('TEST', False)
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://mongo:27017')
DATABASE_NAME = os.environ.get('DATABASE', 'movies_db')

# OMDB API
OMDB_BASE_URL = os.environ.get('OMDB_BASE_URL', 'http://www.omdbapi.com/')
OMDB_APIKEY = os.environ.get('OMDB_APIKEY', '948bd52f')
