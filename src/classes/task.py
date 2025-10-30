from sqlalchemy import Column, String, DateTime, Boolean, event
from src.base_class import Base, default_uuid

from src.enums import TaskStatus

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(String, primary_key=True, default=default_uuid)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime)
    status = Column(String, default=TaskStatus.CREATED)
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Task, 'before_insert')
@event.listens_for(Task, 'before_update')
def validate_task(mapper, connection, target):
    from src.validators.task import TaskValidator
    TaskValidator().validate(target)
