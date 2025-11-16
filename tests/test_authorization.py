import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.controllers.users import UserCtrl


# Convenience method to get authentication headers without bloating the tests
def get_auth_header(client: TestClient, test_user_data: dict):
    login_data = {"username": test_user_data["email"], "password": test_user_data["password"]}
    response = client.post("/auth/token", data=login_data)
    if response.status_code == 200:
        token = response.json().get("access_token")
        return {"Authorization": f"Bearer {token}"}
    return {}


@pytest.fixture
def test_user_data():
    return {"name": "Test User", "email": "test@example.com", "password": "password123", "timezone": "UTC"}


@pytest.fixture
def created_user(db_session: Session, test_user_data: dict):
    return UserCtrl.create(db=db_session, **test_user_data)


def test_register(client: TestClient):
    user_data = {"name": "Test User", "email": "testuser@example.com", "password": "a-valid-password", "timezone": "UTC"}
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "testuser@example.com"


def test_login_for_access_token(client: TestClient, created_user, test_user_data):
    headers = get_auth_header(client, test_user_data)
    assert "Authorization" in headers
    assert "Bearer" in headers["Authorization"]


def test_read_users_me(client: TestClient, created_user, test_user_data):
    headers = get_auth_header(client, test_user_data)
    response = client.get("/auth/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == test_user_data["email"]
