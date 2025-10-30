from enum import StrEnum

class TaskStatus(StrEnum):
    CREATED = 'created'
    PENDING = 'pending'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'
