from datetime import datetime

from src.classes import Event
from src.interfaces import Validator


class EventValidator(Validator):

    @staticmethod
    def validate(event: Event) -> bool:
        if not isinstance(event, Event):
            raise TypeError("Object must be of type Event")
        if not event.title or len(event.title.strip()) == 0:
            raise ValueError("Event title cannot be empty.")
        if not isinstance(event.start_time, datetime) or not isinstance(event.end_time, datetime):
            raise TypeError("Start and end times must be datetime objects.")
        if event.end_time <= event.start_time:
            raise ValueError("End time must be after start time.")
        return True