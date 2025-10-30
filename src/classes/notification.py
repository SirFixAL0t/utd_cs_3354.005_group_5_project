from sqlalchemy import Column, String, DateTime, Boolean, event
from src.base_class import Base, default_uuid
from datetime import datetime, timezone

class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(String, primary_key=True, default=default_uuid)
    _type = Column(String)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    delivery_status = Column(String)
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Notification, 'before_insert')
@event.listens_for(Notification, 'before_update')
def validate_notification(mapper, connection, target):
    from src.validators.notification import NotificationValidator
    NotificationValidator().validate(target)