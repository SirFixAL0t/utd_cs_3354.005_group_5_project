from typing import Any
from sqlalchemy.orm import Session

from src.classes import Poll
from src.interfaces import PersistentController


class PollCtrl(PersistentController):
    @staticmethod
    def create(db: Session, question: str, options: list[str]) -> Poll:
        """
        Factory to create a Poll
        :param db: The database session
        :param question: The question for the poll
        :param options: The options for the poll
        :return: a new Poll object
        """
        new_poll = Poll(question=question, options=options)
        db.add(new_poll)
        db.commit()
        db.refresh(new_poll)
        return new_poll

    @staticmethod
    def save(record: Poll, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Poll | None:
        return storage.query(Poll).filter(Poll.poll_id == identifier, Poll.deleted == False).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Poll]:
        return storage.query(Poll).filter(*criteria, Poll.deleted == False).all()

    @staticmethod
    def safe_delete(record: Poll, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: Poll, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
