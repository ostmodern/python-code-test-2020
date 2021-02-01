import json
import pytest

from app import views
# (
#     episodes_retrieve_all,
#     episode_retrieve_one,
#     comments_retrieve_all,
#     comment_retrieve_one,
#     comment_delete_one,
#     comment_update_one,
#     comment_create_one,
# )

def test_all_episodes(test_app, monkeypatch):
    test_data = [
        {'season': '1',
         'title': '3 monkeys'},
        {'season': '2',
         'imdbRating': 4.6,
         'title': '2 dogs'},
    ]

    def mock_episodes_retrieve_all():
        return test_data

    monkeypatch.setattr(views, "episodes_retrieve_all", mock_episodes_retrieve_all)

    response = test_app.get("/episodes/")
    assert response.status_code == 200
    assert response.json() == test_data
