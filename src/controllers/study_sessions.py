from typing import Any
from sqlalchemy.orm import Session

from src.classes.study_session import StudySession
from src.interfaces import PersistentController
from src.enums import SessionStatus


class StudySessionCtrl(PersistentController):
    @staticmethod
    def create(db: Session, title: str, owner_id: str) -> StudySession:
        new_session = StudySession(title=title, owner_id=owner_id)
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session

    @staticmethod
    def save(record: StudySession, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> StudySession | None:
        return storage.query(StudySession).filter(StudySession.session_id == identifier, StudySession.deleted == False).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[StudySession]:
        return storage.query(StudySession).filter(*criteria, StudySession.deleted == False).all()

    @staticmethod
    def safe_delete(record: StudySession, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: StudySession, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
