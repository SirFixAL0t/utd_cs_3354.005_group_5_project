from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON, event
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid



class Event(Base):
    __tablename__ = 'events'
    event_id = Column(String, primary_key=True, default=default_uuid)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String)
    calendar_id = Column(String, ForeignKey('calendars.calendar_id'))
    calendar = relationship("Calendar", back_populates="events")
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Event, 'before_insert')
@event.listens_for(Event, 'before_update')
def validate_event(mapper, connection, target):
    from src.validators.event import EventValidator
    EventValidator().validate(target)