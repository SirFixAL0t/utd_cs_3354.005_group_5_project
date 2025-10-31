from src.constants import POLL_OPTION_TEXT_LENGTH
from src.interfaces import Validator
from src.classes.poll_option import PollOption


class PollOptionValidator(Validator):
    def validate(self, poll_option: PollOption) -> bool:
        if not isinstance(poll_option, PollOption):
            raise TypeError("Object must be of type PollOption")
        if not poll_option.option_text or len(poll_option.option_text.strip()) == 0:
            raise ValueError("Poll option text cannot be empty.")
        if len(poll_option.option_text) > POLL_OPTION_TEXT_LENGTH[1]:
            raise ValueError(f"Poll option text cannot exceed {POLL_OPTION_TEXT_LENGTH[1]} characters.")
        return True
