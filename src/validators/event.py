from datetime import datetime

from src.classes.event import Event
from src.interfaces import Validator
from src.constants import CALENDAR_TITLE, SESSION_LOCATION_LENGTH


class EventValidator(Validator):
    def validate(self, event: Event) -> bool:
        if not isinstance(event, Event):
            raise TypeError("Object must be of type Event")

        if not event.title or len(event.title.strip()) < CALENDAR_TITLE[0]:
            raise ValueError(f"Event title must be at least {CALENDAR_TITLE[0]} character.")
        if len(event.title) > CALENDAR_TITLE[1]:
            raise ValueError(f"Event title cannot exceed {CALENDAR_TITLE[1]} characters.")

        if not isinstance(event.start_time, datetime) or not isinstance(event.end_time, datetime):
            raise TypeError("Start and end times must be datetime objects.")
        if event.end_time <= event.start_time:
            raise ValueError("End time must be after start time.")

        if event.location and len(event.location) > SESSION_LOCATION_LENGTH[1]:
            raise ValueError(f"Location cannot exceed {SESSION_LOCATION_LENGTH[1]} characters.")

        return True
