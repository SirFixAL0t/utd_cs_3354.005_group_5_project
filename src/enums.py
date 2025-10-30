from enum import StrEnum, IntFlag, IntEnum


class DeliveryStatus(StrEnum):
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
    FAILED = 'failed'

class TaskStatus(StrEnum):
    CREATED = 'created'
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class Permissions(IntFlag):
    """
    permissions in bit mask:
    """
    WRITE = 1  # 0001
    READ = 2   # 0010
    DELETE = 4 # 0100
    SHARE = 8  # 1000

class NotificationTypes(StrEnum):
    ALERT = 'alert'
    WARNING = 'warning'
    INFO = 'info'
    DEBUG = 'debug'
    SUCCESS = 'success'

class RecurrenceRule(IntEnum):
    NONE = 0
    HOURLY = 1
    DAILY = 2
    WEEKDAYS = 3
    WEEKLY = 4
    BIWEEKLY = 5
    ALT_WEEKLY = 6
    MONTHLY = 7
    QUARTERLY = 8
    YEARLY = 9

class FriendStatus(StrEnum):
    ACTIVE = 'active'
    TERMINATED = 'terminated'
    BLOCKED = 'blocked'

class SessionStatus(StrEnum):
    ACTIVE = 'active'
    TERMINATED = 'terminated'
    FINISHED = 'finished'
    PAUSED = 'paused'
    IN_SESSION = 'in_session'