from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, event, Integer
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid
from src.enums import RecurrenceRule


class Event(Base):
    __tablename__ = 'events'
    event_id = Column(String, primary_key=True, default=default_uuid)
    title = Column(String, nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=False)
    location = Column(String)
    calendar_id = Column(String, ForeignKey('calendars.calendar_id'))
    deleted = Column(Boolean, default=False, nullable=False)
    recurrence_rule = Column(Integer, default=0)
    is_seeded = Column(Boolean, default=False, nullable=False)

    calendar = relationship("Calendar", back_populates="events")
    notifications = relationship("Notification", back_populates="event", cascade="all, delete-orphan")

    @property
    def is_recurrent(self):
        # Here's where we would check for additional rules once we add them
        return self.recurrence_rule not in [RecurrenceRule.NONE]


@event.listens_for(Event, 'before_insert')
@event.listens_for(Event, 'before_update')
def validate_event(mapper, connection, target):
    from src.validators.event import EventValidator
    EventValidator().validate(target)
