from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session

from src.classes import Event
from src.interfaces import PersistentController


class EventCtrl(PersistentController):
    @staticmethod
    def create(
        db: Session,
        title: str,
        start_time: datetime,
        end_time: datetime,
        location: str,
        calendar_id: str,
    ) -> Event:
        """
        Factory to create an Event
        :param db: The database session
        :param title: The title of the event
        :param start_time: The start time of the event
        :param end_time: The end time of the event
        :param location: The location of the event
        :param calendar_id: The ID of the calendar this event belongs to
        :return: a new Event object
        """
        new_event = Event(
            title=title,
            start_time=start_time,
            end_time=end_time,
            location=location,
            calendar_id=calendar_id,
        )
        db.add(new_event)
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
