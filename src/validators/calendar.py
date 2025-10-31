from src.classes.calendar import Calendar, ExternalCalendar
from src.interfaces import Validator
from src.constants import CALENDAR_NAME, CALENDAR_DESCRIPTION


class CalendarValidator(Validator):
    def validate(self, calendar: Calendar) -> bool:
        if not isinstance(calendar, Calendar):
            raise TypeError("Object must be of type Calendar")

        if not calendar.name or len(calendar.name.strip()) < CALENDAR_NAME[0]:
            raise ValueError(f"Calendar name must be at least {CALENDAR_NAME[0]} character.")
        if len(calendar.name) > CALENDAR_NAME[1]:
            raise ValueError(f"Calendar name cannot exceed {CALENDAR_NAME[1]} characters.")

        if calendar.description and len(calendar.description) > CALENDAR_DESCRIPTION[1]:
            raise ValueError(f"Calendar description cannot exceed {CALENDAR_DESCRIPTION[1]} characters.")

        return True


class ExternalCalendarValidator(Validator):
    def validate(self, ext_cal: ExternalCalendar) -> bool:
        if not isinstance(ext_cal, ExternalCalendar):
            raise TypeError("Object must be of type ExternalCalendar")
        if not ext_cal.provider:
            raise ValueError("External calendar must have a provider.")
        return True
