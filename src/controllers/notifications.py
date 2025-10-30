from typing import Any
from sqlalchemy.orm import Session
from datetime import datetime

from src.classes.notification import Notification
from src.interfaces import PersistentController
from src.enums import NotificationTypes


class NotificationCtrl(PersistentController):
    @staticmethod
    def create(
        db: Session,
        event_id: str,
        notification_type: NotificationTypes,
        message: str,
        timestamp: datetime,
    ) -> Notification:
        new_notification = Notification(
            event_id=event_id,
            type=notification_type,
            message=message,
            timestamp=timestamp,
        )
        db.add(new_notification)
        db.commit()
        db.refresh(new_notification)
        return new_notification

    @staticmethod
    def save(record: Notification, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Notification | None:
        return storage.query(Notification).filter(Notification.notification_id == identifier, Notification.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Notification]:
        return storage.query(Notification).filter(*criteria, Notification.deleted.is_(False)).all()

    @staticmethod
    def safe_delete(record: Notification, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: Notification, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
