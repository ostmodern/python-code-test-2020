import uuid
import mock
import mongomock
import pytest

import app

from settings import TEST
from src.models import DATABASE_NAME, db_client

@pytest.fixture
def client():
    yield app.app.test_client()


@pytest.fixture(autouse=True)
def drop_db():
    if not TEST or not isinstance(db_client, mongomock.MongoClient):
        raise RuntimeError("Don't use this outside tests!")
    yield
    db_client.drop_database(DATABASE_NAME)


class TestEpisodes:
    url = '/episodes'

    def test_success(self, client):
        db_client.movies_db.episodes.insert_one(
            {
                "Title": "The North Remembers",
                "Released": "2012-04-01",
                "Episode": "1",
                "imdbRating": "8.8",
                "imdbID": "tt1971833"
            },
        )
        response = client.get(self.url)
        assert response.status_code == 200
        assert "episodes" in response.json
        assert "total" in response.json
        assert response.json.get("total") == 1
