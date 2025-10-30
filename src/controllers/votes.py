from typing import Any
from sqlalchemy.orm import Session

from src.classes.vote import Vote
from src.classes.poll_option import PollOption
from src.controllers.polls import PollCtrl
from src.interfaces import PersistentController


class VoteCtrl(PersistentController):
    @staticmethod
    def create(db: Session, poll_option_id: str, user_id: str) -> Vote:
        option = db.query(PollOption).filter(PollOption.option_id == poll_option_id).first()
        if not option:
            raise ValueError("Invalid poll option ID")

        poll = option.poll
        if not PollCtrl.can_user_vote(poll, user_id, db):
            raise PermissionError("User is not allowed to vote on this poll.")

        new_vote = Vote(poll_option_id=poll_option_id, user_id=user_id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return new_vote

    @staticmethod
    def save(record: Vote, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Vote | None:
        return storage.query(Vote).filter(Vote.vote_id == identifier, Vote.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Vote]:
        return storage.query(Vote).filter(*criteria, Vote.deleted.is_(False)).all()

    @staticmethod
    def safe_delete(record: Vote, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: Vote, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
