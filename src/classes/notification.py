from sqlalchemy import Column, String, DateTime, Boolean, event, ForeignKey, Enum
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid
from datetime import datetime, timezone

from src.enums import DeliveryStatus, NotificationTypes


class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(String, primary_key=True, default=default_uuid)
    event_id = Column(String, ForeignKey('events.event_id'), nullable=False)
    type = Column(Enum(NotificationTypes), nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    delivery_status = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    event = relationship("Event", back_populates="notifications")

    def set_delivery_status(self, status: DeliveryStatus):
        self.delivery_status = status

    def should_trigger(self, date: datetime | None = None) -> bool:
        if date is None:
            date = datetime.now(timezone.utc)

        # Only trigger if time is past and status is pending
        return self.timestamp <= date and self.delivery_status == DeliveryStatus.PENDING


@event.listens_for(Notification, 'before_insert')
@event.listens_for(Notification, 'before_update')
def validate_notification(mapper, connection, target):
    from src.validators.notification import NotificationValidator
    NotificationValidator().validate(target)
