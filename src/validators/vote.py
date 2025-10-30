from src.classes.vote import Vote
from src.interfaces import Validator


class VoteValidator(Validator):
    def validate(self, vote: Vote) -> bool:
        if not isinstance(vote, Vote):
            raise TypeError("Object must be of type Vote")
        if not vote.poll_option_id:
            raise ValueError("A vote must have a selected poll option ID.")
        return True
