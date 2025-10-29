from src.classes import Notification
from src.interfaces import Validator


class NotificationValidator(Validator):

    @staticmethod
    def validate(notification: Notification) -> bool:
        if not isinstance(notification, Notification):
            raise TypeError("Object must be of type Notification")
        if not notification.message or len(notification.message.strip()) == 0:
            raise ValueError("Notification message cannot be empty.")
        return True