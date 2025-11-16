import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.controllers.users import UserCtrl
from src.classes.calendar import Calendar as DBCalendar
from src.classes.event import Event as DBEvent
from datetime import datetime, timedelta, timezone
from tests.test_authorization import get_auth_header
from src.enums import NotificationTypes


@pytest.fixture
def test_user_data():
    return {"name": "Calendar User", "email": "calendar@example.com", "password": "password123", "timezone": "UTC"}


@pytest.fixture
def created_user(db_session: Session, test_user_data: dict):
    return UserCtrl.create(db=db_session, **test_user_data)


@pytest.fixture
def auth_headers(client: TestClient, created_user, test_user_data):
    return get_auth_header(client, test_user_data)


@pytest.fixture
def test_calendar(db_session: Session, created_user):
    calendar = DBCalendar(user_id=created_user.user_id, name="Test Calendar")
    db_session.add(calendar)
    db_session.commit()
    db_session.refresh(calendar)
    return calendar


@pytest.fixture
def test_event(db_session: Session, test_calendar: DBCalendar):
    event = DBEvent(
        title="Test Event",
        start_time=datetime.now(timezone.utc),
        end_time=datetime.now(timezone.utc) + timedelta(hours=1),
        calendar_id=test_calendar.calendar_id,
    )
    db_session.add(event)
    db_session.commit()
    db_session.refresh(event)
    return event


def test_create_event(client: TestClient, auth_headers: dict):
    event_data = {
        "title": "New Event",
        "start_time": "2024-01-01T10:00:00Z",
        "end_time": "2024-01-01T11:00:00Z",
    }
    response = client.post("/calendar/events", headers=auth_headers, json=event_data)
    assert response.status_code == 200
    assert response.json()["title"] == "New Event"


def test_get_event(client: TestClient, auth_headers: dict, test_event: DBEvent):
    response = client.get(f"/calendar/events/{test_event.event_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Event"


def test_update_event(client: TestClient, auth_headers: dict, test_event: DBEvent):
    update_data = {"title": "Updated Event"}
    response = client.put(f"/calendar/events/{test_event.event_id}", headers=auth_headers, json=update_data)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Event"


def test_add_notification_to_event(client: TestClient, auth_headers: dict, test_event: DBEvent):
    notification_data = {
        "type": NotificationTypes.ALERT.value,
        "message": "Test Notification",
        "timestamp": "2024-01-01T09:00:00Z",
    }
    response = client.post(
        f"/calendar/events/{test_event.event_id}/notifications",
        headers=auth_headers,
        json=notification_data,
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Test Notification"
