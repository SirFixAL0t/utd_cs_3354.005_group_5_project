from datetime import datetime
from typing import Any

from src.classes import Task
from src.enums import TaskStatus
from src.interfaces import PersistentController


class TaskCtrl(PersistentController):

    @staticmethod
    def create(
            title: str,
            description: str,
            due_date: datetime,
            status: TaskStatus
    ) -> Task:
        """
        Factory to create a task
        :param title: the Task title
        :param description: What's the task about
        :param due_date: When's the task due?
        :param status: The task status on creation
        :return: a new Task object
        """
        return Task(title, description, due_date, status)

    @staticmethod
    def save(record: Any, storage: Any) -> bool:
        # @TODO implement method
        pass

    @staticmethod
    def load(identifier: Any, storage: Any) -> Any:
        # @TODO implement method
        pass

    @staticmethod
    def search(criteria: list[Any], storage: Any) -> list[Any]:
        # @TODO implement method
        pass

    @staticmethod
    def safe_delete(record: Any, storage: Any) -> bool:
        # @TODO implement method
        pass

    @staticmethod
    def permanent_delete(record: Any, storage: Any) -> bool:
        # @TODO implement method
        pass
