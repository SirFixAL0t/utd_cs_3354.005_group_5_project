import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.controllers.users import UserCtrl
from tests.test_authorization import get_auth_header


@pytest.fixture
def test_user_data():
    return {"name": "Settings User", "email": "settings@example.com", "password": "password123", "timezone": "UTC"}


@pytest.fixture
def created_user(db_session: Session, test_user_data: dict):
    return UserCtrl.create(db=db_session, **test_user_data)


def test_read_settings(client: TestClient, created_user, test_user_data):
    headers = get_auth_header(client, test_user_data)
    response = client.get("/settings/", headers=headers)
    assert response.status_code == 200
    assert response.json()["theme"] == "dark"
    assert response.json()["timezone"] == "UTC"


def test_update_settings(client: TestClient, created_user, test_user_data):
    headers = get_auth_header(client, test_user_data)
    response = client.put("/settings/", headers=headers, json={"theme": "light", "timezone": "PST"})
    assert response.status_code == 200
    assert response.json()["theme"] == "light"
    assert response.json()["timezone"] == "PST"
