import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture
def client():
    original = copy.deepcopy(app_module.activities)
    test_client = TestClient(app_module.app)
    yield test_client
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(original))


def test_get_activities_returns_activity_list(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    payload = response.json()
    assert expected_activity in payload
    assert payload[expected_activity]["participants"]


def test_signup_for_activity_success(client):
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_for_activity_rejects_duplicate_email(client):
    # Arrange
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 409
    assert response.json()["detail"] == "Student already signed up"


def test_unregister_participant_success(client):
    # Arrange
    email_to_remove = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": email_to_remove},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email_to_remove} from Chess Club"
    assert email_to_remove not in client.get("/activities").json()["Chess Club"]["participants"]


def test_unregister_participant_missing_email_fails(client):
    # Arrange
    missing_email = "ghost@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": missing_email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
