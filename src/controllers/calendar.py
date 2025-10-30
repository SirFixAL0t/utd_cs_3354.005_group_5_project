from typing import Any
from sqlalchemy.orm import Session

from src.classes.event import Event
from src.classes.calendar import Calendar
from src.interfaces import PersistentController


class CalendarCtrl(PersistentController):
    @staticmethod
    def create(
        db: Session,
        name: str,
        calendar_type: str,
        visibility: str,
        color: str,
        shared: bool,
        user_id: str,
        events: list[Event] | None = None,
    ) -> Calendar:
        """
        Factory to create a Calendar
        :param db: The database session
        :param name: The name of the calendar
        :param calendar_type: The type of the calendar
        :param visibility: The visibility of the calendar
        :param color: The color of the calendar
        :param shared: Whether the calendar is shared
        :param user_id: The ID of the user who owns the calendar
        :param events: A list of events to initialize the calendar with
        :return: a new Calendar object
        """
        if events is None:
            events = []
        new_calendar = Calendar(
            name=name,
            type=calendar_type,
            visibility=visibility,
            color=color,
            shared=shared,
            user_id=user_id,
        )
        db.add(new_calendar)
        db.commit()
        db.refresh(new_calendar)
        return new_calendar

    @staticmethod
    def save(record: Calendar, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Calendar | None:
        return storage.query(Calendar).filter(Calendar.calendar_id == identifier, Calendar.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Calendar]:
        return storage.query(Calendar).filter(*criteria, Calendar.deleted.is_(False)).all()

    @staticmethod
    def safe_delete(record: Calendar, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: Calendar, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
