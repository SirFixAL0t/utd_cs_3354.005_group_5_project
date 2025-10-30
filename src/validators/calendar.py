from src.classes.calendar import Calendar, ExternalCalendar
from src.interfaces import Validator


class CalendarValidator(Validator):

    @staticmethod
    def validate(calendar: Calendar) -> bool:
        if not isinstance(calendar, Calendar):
            raise TypeError("Object must be of type Calendar")
        if not calendar.name or len(calendar.name.strip()) == 0:
            raise ValueError("Calendar name cannot be empty.")
        return True

class ExternalCalendarValidator(Validator):

    @staticmethod
    def validate(ext_cal: ExternalCalendar) -> bool:
        if not isinstance(ext_cal, ExternalCalendar):
            raise TypeError("Object must be of type ExternalCalendar")
        if not ext_cal.provider:
            raise ValueError("External calendar must have a provider.")
        return True