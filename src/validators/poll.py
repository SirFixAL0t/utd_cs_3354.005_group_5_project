from src.classes.poll import Poll
from src.interfaces import Validator


class PollValidator(Validator):

    def validate(self, poll: Poll) -> bool:
        if not isinstance(poll, Poll):
            raise TypeError("Object must be of type Poll")
        if not poll.question or len(poll.question.strip()) == 0:
            raise ValueError("Poll question cannot be empty.")
        return True
