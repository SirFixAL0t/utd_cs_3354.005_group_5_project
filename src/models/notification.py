from pydantic import BaseModel, ConfigDict
from datetime import datetime
from src.enums import NotificationTypes, DeliveryStatus

class NotificationBase(BaseModel):
    type: NotificationTypes
    message: str
    timestamp: datetime

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    notification_id: str
    event_id: str
    delivery_status: DeliveryStatus
    deleted: bool
    model_config = ConfigDict(from_attributes=True)
