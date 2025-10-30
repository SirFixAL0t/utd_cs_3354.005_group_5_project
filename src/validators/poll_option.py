from src.interfaces import Validator
from src.classes.poll_option import PollOption


class PollOptionValidator(Validator):
    def validate(self, poll_option: PollOption) -> bool:
        if not isinstance(poll_option, PollOption):
            raise TypeError("Object must be of type PollOption")
        if not poll_option.option_text or len(poll_option.option_text.strip()) == 0:
            raise ValueError("Poll option text cannot be empty.")
        return True
