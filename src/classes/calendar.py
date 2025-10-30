from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON, event
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid


class Calendar(Base):
    __tablename__ = 'calendars'
    calendar_id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False)
    type = Column(String)
    visibility = Column(String)
    color = Column(String)
    shared = Column(Boolean, default=False)
    events = relationship("Event", back_populates="calendar")
    user_id = Column(String, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="calendars")
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Calendar, 'before_insert')
@event.listens_for(Calendar, 'before_update')
def validate_calendar(mapper, connection, target):
    from src.validators.calendar import CalendarValidator
    CalendarValidator().validate(target)

class ExternalCalendar(Base):
    __tablename__ = 'external_calendars'
    account_id = Column(String, primary_key=True, default=default_uuid)
    provider = Column(String)
    accessToken = Column(String)
    refreshToken = Column(String)
    last_sync = Column(DateTime)
    deleted = Column(Boolean, default=False, nullable=False)

    def get_provider(self) -> str:
        return self.provider

    def get_last_sync(self) -> datetime:
        return self.last_sync



@event.listens_for(ExternalCalendar, 'before_insert')
@event.listens_for(ExternalCalendar, 'before_update')
def validate_external_calendar(mapper, connection, target):
    from src.validators.calendar import ExternalCalendarValidator
    ExternalCalendarValidator().validate(target)