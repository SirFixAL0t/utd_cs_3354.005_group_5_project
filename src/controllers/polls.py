from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy import func

from src.classes.poll import Poll
from src.classes.poll_option import PollOption
from src.classes.vote import Vote
from src.interfaces import PersistentController


class PollCtrl(PersistentController):
    @staticmethod
    def create(db: Session, question: str, owner_id: str, options: list[str], allow_multi_votes: bool = False) -> Poll:
        """
        Factory to create a Poll
        :param db: The database session
        :param question: The question for the poll
        :param owner_id: The ID of the user who owns the poll
        :param options: A list of strings for the poll options
        :param allow_multi_votes: Whether to allow multiple votes from a single user
        :return: a new Poll object
        """
        new_poll = Poll(question=question, owner_id=owner_id, allow_multi_votes=allow_multi_votes)
        db.add(new_poll)
        db.flush()  # Use flush to get the poll_id before committing

        for option_text in options:
            new_option = PollOption(poll_id=new_poll.poll_id, option_text=option_text)
            db.add(new_option)

        db.commit()
        db.refresh(new_poll)
        return new_poll

    @staticmethod
    def get_most_voted_option(poll: Poll, db: Session) -> PollOption | None:
        return (
            db.query(PollOption)
            .join(Vote)
            .filter(PollOption.poll_id == poll.poll_id)
            .group_by(PollOption.option_id)
            .order_by(func.count(Vote.vote_id).desc())
            .first()
        )

    @staticmethod
    def get_votes(poll: Poll, db: Session) -> list[type[Vote]]:
        return db.query(Vote).join(PollOption).filter(PollOption.poll_id == poll.poll_id).all()

    @staticmethod
    def user_has_voted(poll: Poll, user_id: str, db: Session) -> bool:
        return (
            db.query(Vote)
            .join(PollOption)
            .filter(PollOption.poll_id == poll.poll_id, Vote.user_id == user_id)
            .count()
            > 0
        )

    @staticmethod
    def can_user_vote(poll: Poll, user_id: str, db: Session) -> bool:
        if poll.is_closed:
            return False
        if poll.allow_multi_votes:
            return True
        return not PollCtrl.user_has_voted(poll, user_id, db)

    @staticmethod
    def close_poll(poll: Poll, db: Session) -> None:
        poll.is_closed = True
        db.commit()

    @staticmethod
    def save(record: Poll, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Poll | None:
        return storage.query(Poll).filter(Poll.poll_id == identifier, Poll.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[type[Poll]]:
        return storage.query(Poll).filter(*criteria, Poll.deleted.is_(False)).all()

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
