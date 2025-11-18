from pydantic import BaseModel, ConfigDict
from typing import Optional

class CalendarBase(BaseModel):
    name: str
    code: str
    type: Optional[str] = None
    visibility: Optional[str] = None
    color: Optional[str] = None
    shared: bool = False
    description: Optional[str] = None

class CalendarCreate(CalendarBase):
    pass

class CalendarUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    visibility: Optional[str] = None
    color: Optional[str] = None
    shared: Optional[bool] = None
    description: Optional[str] = None

class Calendar(CalendarBase):
    calendar_id: str
    user_id: str
    deleted: bool
    is_seeded: bool
    model_config = ConfigDict(from_attributes=True)
