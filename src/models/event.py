from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional
from src.enums import RecurrenceRule

class EventBase(BaseModel):
    title: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    recurrence_rule: RecurrenceRule = RecurrenceRule.NONE

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    title: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    recurrence_rule: Optional[RecurrenceRule] = None


class Event(EventBase):
    event_id: str
    calendar_id: str
    deleted: bool
    model_config = ConfigDict(from_attributes=True)
