from typing import Any
from sqlalchemy.orm import Session

from src.classes.vote import Vote
from src.interfaces import PersistentController


class VoteCtrl(PersistentController):
    @staticmethod
    def create(db: Session, poll_option_id: str, user_id: str) -> Vote:
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
        return storage.query(Vote).filter(Vote.vote_id == identifier, Vote.deleted == False).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Vote]:
        return storage.query(Vote).filter(*criteria, Vote.deleted == False).all()

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
