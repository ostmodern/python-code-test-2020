import uuid

import mongomock
import pymongo

from settings import DATABASE_NAME, MONGO_URI, TEST


def get_client():
    if TEST:
        return mongomock.MongoClient()
    else:
        return pymongo.MongoClient(
            host=MONGO_URI
        )


db_client = get_client()
db = db_client[DATABASE_NAME]


class BaseModel:
    collection = None

    def insert_one(self, data_dict: dict):
        data_dict['_id'] = uuid.uuid4()
        result = self.collection.insert_one(data_dict)
        return result.acknowledged

    def find_by_imdb_id(self, imdb_id):
        query = {'imdbID': imdb_id}
        result = self.collection.find_one(query, {'_id': 0})
        return result

    def find(self, query):
        result = self.collection.find(query, {'_id': 0})
        return result


class Movie(BaseModel):
    collection = db['movies']


class Episode(BaseModel):
    collection = db['episodes']


class Comment(BaseModel):
    collection = db['comments']

    def find(self, query):
        result = self.collection.find(query)
        return result

    def update(self, comment_id, data):
        result = self.collection.update_one({'_id': comment_id}, {'$set': data})
        return result.modified_count

    def delete_one(self, comment_id):
        result = self.collection.delete_one({'_id': comment_id})
        return result.deleted_count
