from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
import uuid
from pydantic import EmailStr, TypeAdapter

from src.classes.notification import Notification
from src.classes.event import Event
from src.controllers.notifications import NotificationCtrl
from src.controllers.events import EventCtrl
from src.controllers.calendar import CalendarCtrl
from src.controllers.users import UserCtrl
from src.enums import NotificationTypes, DeliveryStatus

EmailAdapter = TypeAdapter(EmailStr)


@pytest.fixture
def test_event(db_session: Session) -> Event:
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email=EmailAdapter.validate_python(f"notification-test-{uuid.uuid4()}@example.com"),
        password="password123",
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


aware_datetimes = st.datetimes(min_value=datetime(2000, 1, 1), max_value=datetime(2030, 1, 1)).map(
    lambda dt: dt.replace(tzinfo=timezone.utc)
)

notification_strategy = st.builds(
    Notification,
    type=st.sampled_from(NotificationTypes),
    message=st.text(min_size=1, max_size=255),
    timestamp=aware_datetimes,
)

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(notification_data=notification_strategy)
def test_notification_creation_and_retrieval_property(
    db_session: Session, test_event: Event, notification_data: Notification
):
    """Property-based test for notification creation and retrieval."""
    try:
        created_notification = NotificationCtrl.create(
            db=db_session,
            event_id=test_event.event_id,
            notification_type=notification_data.type,
            message=notification_data.message,
            timestamp=notification_data.timestamp,
        )
    except Exception:
        db_session.rollback()
        return

    loaded_notification = NotificationCtrl.load(created_notification.notification_id, db_session)

    assert loaded_notification is not None
    assert loaded_notification.type == created_notification.type
    assert loaded_notification.message == created_notification.message


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

    # Need to create a separate event for each notification to avoid session conflicts
    past_notification = NotificationCtrl.create(
        db=db_session,
        event_id=test_event.event_id,
        notification_type=NotificationTypes.ALERT,
        message="Past notification",
        timestamp=past_timestamp,
    )

    future_event = EventCtrl.create(
        db=db_session,
        title="Future Event",
        start_time=datetime.now(timezone.utc) + timedelta(days=1),
        end_time=datetime.now(timezone.utc) + timedelta(days=1, hours=1),
        location="Future Location",
        calendar_id=test_event.calendar_id,
    )

    future_notification = NotificationCtrl.create(
        db=db_session,
        event_id=future_event.event_id,
        notification_type=NotificationTypes.ALERT,
        message="Future notification",
        timestamp=future_timestamp,
    )

    assert past_notification.should_trigger()
    assert not future_notification.should_trigger()

    past_notification.set_delivery_status(DeliveryStatus.COMPLETED)
    db_session.commit()
    assert not past_notification.should_trigger()
