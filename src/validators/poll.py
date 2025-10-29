from src.classes import Poll
from src.interfaces import Validator


class PollValidator(Validator):

    @staticmethod
    def validate(poll: Poll) -> bool:
        if not isinstance(poll, Poll):
            raise TypeError("Object must be of type Poll")
        if not poll.question or len(poll.question.strip()) == 0:
            raise ValueError("Poll question cannot be empty.")
        if not isinstance(poll.options, list) or len(poll.options) < 2:
            raise ValueError("Poll must have at least two options.")
        return True