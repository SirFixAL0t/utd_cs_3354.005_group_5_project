from sqlalchemy.orm import Session
import pytest

from src.classes import Calendar, User
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


def test_calendar_creation(db_session: Session, test_user: User):
    """Black-box test for calendar creation."""
    calendar = CalendarCtrl.create(
        db=db_session,
        name="Test Calendar",
        calendar_type="personal",
        visibility="private",
        color="#FFFFFF",
        shared=False,
        user_id=test_user.user_id,
    )
    assert calendar.calendar_id
    assert calendar.name == "Test Calendar"
    assert not calendar.deleted
    assert calendar.user_id == test_user.user_id


def test_calendar_creation_empty_name(db_session: Session, test_user: User):
    """Boundary test for calendar creation with an empty name."""
    with pytest.raises(Exception):
        CalendarCtrl.create(
            db=db_session,
            name="",
            calendar_type="personal",
            visibility="private",
            color="#FFFFFF",
            shared=False,
            user_id=test_user.user_id,
        )


def test_calendar_soft_delete(db_session: Session, test_user: User):
    """White-box test for calendar soft delete."""
    calendar = CalendarCtrl.create(
        db=db_session,
        name="Test Calendar",
        calendar_type="personal",
        visibility="private",
        color="#FFFFFF",
        shared=False,
        user_id=test_user.user_id,
    )
    CalendarCtrl.safe_delete(calendar, db_session)
    deleted_calendar = CalendarCtrl.load(calendar.calendar_id, db_session)
    assert deleted_calendar is None

    # Verify that the calendar is still in the database but marked as deleted
    deleted_calendar_in_db = (
        db_session.query(Calendar).filter(Calendar.calendar_id == calendar.calendar_id).first()
    )
    assert deleted_calendar_in_db
    assert deleted_calendar_in_db.deleted
