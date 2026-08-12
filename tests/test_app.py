from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_success():
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" in response.json()["message"]

    activity = client.get("/activities").json()["Chess Club"]
    assert "michael@mergington.edu" not in activity["participants"]


def test_unregister_participant_missing_email_fails():
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=ghost@mergington.edu"
    )

    assert response.status_code == 404
