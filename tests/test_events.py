from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import pytest

from src.classes.event import Event
from src.classes.calendar import Calendar
from src.classes.user import User
from src.controllers.events import EventCtrl
from src.controllers.calendar import CalendarCtrl
from src.controllers.users import UserCtrl
from src.enums import RecurrenceRule
from src.constants import CALENDAR_TITLE


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test-event@example.com",
        pw="password123",
        timezone="UTC",
    )


@pytest.fixture
def test_calendar(db_session: Session, test_user: User) -> Calendar:
    return CalendarCtrl.create(
        db=db_session,
        name="Test Calendar for Events",
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


def test_event_creation_empty_title(db_session: Session, test_calendar: Calendar):
    """Boundary test for event creation with an empty title."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=1)
    with pytest.raises(ValueError):
        EventCtrl.create(
            db=db_session,
            title="",
            start_time=start_time,
            end_time=end_time,
            location="Test Location",
            calendar_id=test_calendar.calendar_id,
        )


def test_event_creation_long_title(db_session: Session, test_calendar: Calendar):
    """Boundary test for event creation with a title that is too long."""
    long_title = "a" * (CALENDAR_TITLE[1] + 1)
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=1)
    with pytest.raises(ValueError):
        EventCtrl.create(
            db=db_session,
            title=long_title,
            start_time=start_time,
            end_time=end_time,
            location="Test Location",
            calendar_id=test_calendar.calendar_id,
        )


def test_event_creation_invalid_time(db_session: Session, test_calendar: Calendar):
    """Boundary test for event creation with an invalid time."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time - timedelta(hours=1)  # End time before start time
    with pytest.raises(ValueError):
        EventCtrl.create(
            db=db_session,
            title="Test Event",
            start_time=start_time,
            end_time=end_time,
            location="Test Location",
            calendar_id=test_calendar.calendar_id,
        )


def test_event_recurrence(db_session: Session, test_calendar: Calendar):
    """Test creating an event with a recurrence rule."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=1)
    event = EventCtrl.create(
        db=db_session,
        title="Recurring Event",
        start_time=start_time,
        end_time=end_time,
        location="Test Location",
        calendar_id=test_calendar.calendar_id,
        recurrence_rule=RecurrenceRule.DAILY,
    )
    assert event.recurrence_rule == RecurrenceRule.DAILY
    assert event.is_recurrent


def test_event_soft_delete(db_session: Session, test_calendar: Calendar):
    """White-box test for event soft delete."""
    start_time = datetime.now(timezone.utc)
    end_time = start_time + timedelta(hours=1)
    event = EventCtrl.create(
        db=db_session,
        title="To Be Deleted Event",
        start_time=start_time,
        end_time=end_time,
        location="Test Location",
        calendar_id=test_calendar.calendar_id,
    )
    EventCtrl.safe_delete(event, db_session)
    deleted_event = EventCtrl.load(event.event_id, db_session)
    assert deleted_event is None

    deleted_event_in_db = db_session.query(Event).filter(Event.event_id == event.event_id).first()
    assert deleted_event_in_db
    assert deleted_event_in_db.deleted
