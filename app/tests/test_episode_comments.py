from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_delete_non_existing_comment():
    response = client.delete("/series/1/episodes/1/comments/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Episode comment not found."}
