from datetime import datetime
from typing import Any
from sqlalchemy.orm import Session

from src.classes import Task
from src.enums import TaskStatus
from src.interfaces import PersistentController


class TaskCtrl(PersistentController):

    @staticmethod
    def create(
            db: Session,
            title: str,
            description: str,
            due_date: datetime,
            status: TaskStatus
    ) -> Task:
        """
        Factory to create a task
        :param db: The database session
        :param title: the Task title
        :param description: What's the task about
        :param due_date: When's the task due?
        :param status: The task status on creation
        :return: a new Task object
        """
        new_task = Task(title=title, description=description, due_date=due_date, status=status)
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        return new_task

    @staticmethod
    def save(record: Task, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Task | None:
        return storage.query(Task).filter(Task.task_id == identifier, Task.deleted == False).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Task]:
        return storage.query(Task).filter(*criteria, Task.deleted == False).all()

    @staticmethod
    def safe_delete(record: Task, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: Task, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
