from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import pytest

from src.classes.event import Event
from src.controllers.notifications import NotificationCtrl
from src.controllers.events import EventCtrl
from src.controllers.calendar import CalendarCtrl
from src.controllers.users import UserCtrl
from src.enums import NotificationTypes, DeliveryStatus


@pytest.fixture
def test_event(db_session: Session) -> Event:
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="notification-test@example.com",
        pw="password123",
        timezone="UTC",
    )
    calendar = CalendarCtrl.create(
        db=db_session,
        name="Test Calendar",
        calendar_type="personal",
        visibility="private",
        color="#FFFFFF",
        shared=False,
        user_id=user.user_id,
    )
    start_time = datetime.now(timezone.utc) + timedelta(hours=1)
    end_time = start_time + timedelta(hours=1)
    return EventCtrl.create(
        db=db_session,
        title="Test Event for Notifications",
        start_time=start_time,
        end_time=end_time,
        location="Test Location",
        calendar_id=calendar.calendar_id,
    )


def test_notification_creation(db_session: Session, test_event: Event):
    """Black-box test for notification creation."""
    timestamp = test_event.start_time - timedelta(minutes=30)
    notification = NotificationCtrl.create(
        db=db_session,
        event_id=test_event.event_id,
        notification_type=NotificationTypes.ALERT,
        message="Test notification message",
        timestamp=timestamp,
    )
    assert notification.notification_id
    assert notification.type == NotificationTypes.ALERT
    assert notification.delivery_status == DeliveryStatus.PENDING


def test_notification_creation_empty_message(db_session: Session, test_event: Event):
    """Boundary test for notification creation with an empty message."""
    timestamp = test_event.start_time - timedelta(minutes=30)
    with pytest.raises(ValueError):
        NotificationCtrl.create(
            db=db_session,
            event_id=test_event.event_id,
            notification_type=NotificationTypes.ALERT,
            message="",
            timestamp=timestamp,
        )


def test_notification_should_trigger(db_session: Session, test_event: Event):
    """Test the should_trigger method."""
    past_timestamp = datetime.now(timezone.utc) - timedelta(minutes=1)
    future_timestamp = datetime.now(timezone.utc) + timedelta(minutes=1)

    past_notification = NotificationCtrl.create(
        db=db_session,
        event_id=test_event.event_id,
        notification_type=NotificationTypes.ALERT,
        message="Past notification",
        timestamp=past_timestamp,
    )

    future_notification = NotificationCtrl.create(
        db=db_session,
        event_id=test_event.event_id,
        notification_type=NotificationTypes.ALERT,
        message="Future notification",
        timestamp=future_timestamp,
    )

    assert past_notification.should_trigger()
    assert not future_notification.should_trigger()

    past_notification.set_delivery_status(DeliveryStatus.COMPLETED)
    assert not past_notification.should_trigger()
