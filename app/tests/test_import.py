from app.utils import get_episodes


def test_import_from_omdb_api():
    assert len(get_episodes()) > 0
