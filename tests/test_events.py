from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import pytest

from src.classes.event import Event
from src.classes.calendar import Calendar
from src.classes.user import User
from src.controllers.events import EventCtrl
from src.controllers.calendar import CalendarCtrl
from src.controllers.users import UserCtrl


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test@example.com",
        pw="password",
        timezone="UTC",
    )


@pytest.fixture
def test_calendar(db_session: Session, test_user: User) -> Calendar:
    return CalendarCtrl.create(
        db=db_session,
        name="Test Calendar",
        calendar_type="personal",
        visibility="private",
        color="#FFFFFF",
        shared=False,
        user_id=test_user.user_id,
    )


def test_event_creation(db_session: Session, test_calendar: Calendar):
    """Black-box test for event creation."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=1)
    event = EventCtrl.create(
        db=db_session,
        title="Test Event",
        start_time=start_time,
        end_time=end_time,
        location="Test Location",
        calendar_id=test_calendar.calendar_id,
    )
    assert event.event_id
    assert event.title == "Test Event"
    assert not event.deleted
    assert event.calendar_id == test_calendar.calendar_id


def test_event_creation_invalid_time(db_session: Session, test_calendar: Calendar):
    """Boundary test for event creation with an invalid time."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time - timedelta(hours=1)  # End time before start time
    with pytest.raises(Exception):
        EventCtrl.create(
            db=db_session,
            title="Test Event",
            start_time=start_time,
            end_time=end_time,
            location="Test Location",
            calendar_id=test_calendar.calendar_id,
        )


def test_event_soft_delete(db_session: Session, test_calendar: Calendar):
    """White-box test for event soft delete."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=1)
    event = EventCtrl.create(
        db=db_session,
        title="Test Event",
        start_time=start_time,
        end_time=end_time,
        location="Test Location",
        calendar_id=test_calendar.calendar_id,
    )
    EventCtrl.safe_delete(event, db_session)
    deleted_event = EventCtrl.load(event.event_id, db_session)
    assert deleted_event is None

    # Verify that the event is still in the database but marked as deleted
    deleted_event_in_db = db_session.query(Event).filter(Event.event_id == event.event_id).first()
    assert deleted_event_in_db
    assert deleted_event_in_db.deleted
