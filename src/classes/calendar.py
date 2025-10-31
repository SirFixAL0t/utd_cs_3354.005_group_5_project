from datetime import datetime

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, event, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid
from src.enums import Permissions


class CalendarPermission(Base):
    __tablename__ = 'calendar_permissions'
    permission_id = Column(String, primary_key=True, default=default_uuid)
    calendar_id = Column(String, ForeignKey('calendars.calendar_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    permission_flag = Column(Integer, nullable=False, default=0)

    calendar = relationship("Calendar", back_populates="permissions")
    user = relationship("User")

    def can_access(self) -> bool:
        return self.can_write() or self.can_share() or self.can_read() or self.can_delete()

    def can_read(self) -> bool:
        return self.permission_flag & Permissions.READ == Permissions.READ

    def can_write(self):
        return self.permission_flag & Permissions.WRITE == Permissions.WRITE

    def can_share(self):
        return self.permission_flag & Permissions.SHARE == Permissions.SHARE

    def can_delete(self):
        return self.permission_flag & Permissions.DELETE == Permissions.DELETE


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
    description = Column(String, nullable=True)
    permissions = relationship("CalendarPermission", back_populates="calendar", cascade="all, delete-orphan")

    __table_args__ = (UniqueConstraint('name', 'user_id', name='_user_name_uc'),)

    def is_shared(self) -> bool:
        return self.shared

    def share(self, status: bool = True) -> None:
        self.shared = status


class ExternalCalendar(Base):
    __tablename__ = 'external_calendars'
    account_id = Column(String, primary_key=True, default=default_uuid)
    provider = Column(String)
    accessToken = Column(String)
    refreshToken = Column(String)
    last_sync = Column(DateTime(timezone=True))
    deleted = Column(Boolean, default=False, nullable=False)

    def get_provider(self) -> str:
        return self.provider

    def get_last_sync(self) -> datetime:
        return self.last_sync


@event.listens_for(Calendar, 'before_insert')
@event.listens_for(Calendar, 'before_update')
def validate_calendar(mapper, connection, target):
    from src.validators.calendar import CalendarValidator
    CalendarValidator().validate(target)

@event.listens_for(ExternalCalendar, 'before_insert')
@event.listens_for(ExternalCalendar, 'before_update')
def validate_external_calendar(mapper, connection, target):
    from src.validators.calendar import ExternalCalendarValidator
    ExternalCalendarValidator().validate(target)
