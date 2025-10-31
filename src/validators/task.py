from src.classes.task import Task
from src.interfaces import Validator
from src.constants import CALENDAR_TITLE


class TaskValidator(Validator):
    def validate(self, task: Task) -> bool:
        if not isinstance(task, Task):
            raise TypeError("Object must be of type Task")

        if not task.title or len(task.title.strip()) < CALENDAR_TITLE[0]:
            raise ValueError(f"Task title must be at least {CALENDAR_TITLE[0]} character.")
        if len(task.title) > CALENDAR_TITLE[1]:
            raise ValueError(f"Task title cannot exceed {CALENDAR_TITLE[1]} characters.")

        return True
