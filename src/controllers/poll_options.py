from typing import Any
from sqlalchemy.orm import Session

from src.classes.poll_option import PollOption
from src.interfaces import PersistentController


class PollOptionCtrl(PersistentController):
    @staticmethod
    def create(db: Session, poll_id: str, option_text: str) -> PollOption:
        new_option = PollOption(poll_id=poll_id, option_text=option_text)
        db.add(new_option)
        db.commit()
        db.refresh(new_option)
        return new_option

    @staticmethod
    def save(record: PollOption, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> PollOption | None:
        return storage.query(PollOption).filter(PollOption.option_id == identifier, PollOption.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[PollOption]:
        return storage.query(PollOption).filter(*criteria, PollOption.deleted.is_(False)).all()

    @staticmethod
    def safe_delete(record: PollOption, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: PollOption, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
