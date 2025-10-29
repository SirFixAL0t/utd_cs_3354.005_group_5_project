from src.classes import Vote
from src.interfaces import Validator


class VoteValidator(Validator):
    @staticmethod
    def validate(vote: Vote) -> bool:
        if not isinstance(vote, Vote):
            raise TypeError("Object must be of type Vote")
        if not vote.selected_option:
            raise ValueError("A vote must have a selected option.")
        return True