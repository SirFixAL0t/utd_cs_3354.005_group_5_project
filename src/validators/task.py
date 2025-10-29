from src.classes import Task
from src.interfaces import Validator


class TaskValidator(Validator):

    class TaskValidator(Validator):
        @staticmethod
        def validate(task: Task) -> bool:
            if not isinstance(task, Task):
                raise TypeError("Object must be of type Task")
            if not task.title or len(task.title.strip()) == 0:
                raise ValueError("Task title cannot be empty.")
            return True
