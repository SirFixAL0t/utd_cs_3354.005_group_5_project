from datetime import datetime, timedelta
from typing import Any
from sqlalchemy.orm import Session

from src.classes.event import Event
from src.classes.notification import Notification
from src.interfaces import PersistentController
from src.enums import NotificationTypes


class EventCtrl(PersistentController):
    @staticmethod
    def create(
        db: Session,
        title: str,
        start_time: datetime,
        end_time: datetime,
        location: str,
        calendar_id: str,
        recurrence_rule: int = 0,
    ) -> Event:
        """
        Factory to create an Event
        :param db: The database session
        :param title: The title of the event
        :param start_time: The start time of the event
        :param end_time: The end time of the event
        :param location: The location of the event
        :param calendar_id: The ID of the calendar this event belongs to
        :param recurrence_rule: The recurrence rule for the event
        :return: a new Event object
        """
        new_event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            calendar_id=calendar_id,
            recurrence_rule=recurrence_rule,
        )
        db.add(new_event)
        db.flush()  # Flush to get the event_id

        # Create a default notification 15 minutes before the event
        notification_time = start_time - timedelta(minutes=15)
        default_notification = Notification(
            event_id=new_event.event_id,
            type=NotificationTypes.ALERT,
            message=f"Reminder: {title} is starting soon.",
            timestamp=notification_time,
        )
        db.add(default_notification)

        db.commit()
        db.refresh(new_event)
        return new_event

    @staticmethod
    def save(record: Event, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Event | None:
        return storage.query(Event).filter(Event.event_id == identifier, Event.deleted == False).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Event]:
        return storage.query(Event).filter(*criteria, Event.deleted == False).all()

    @staticmethod
    def safe_delete(record: Event, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: Event, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
