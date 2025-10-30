from typing import Any
from sqlalchemy.orm import Session

from src.classes.study_session_member import StudySessionMember
from src.interfaces import PersistentController


class StudySessionMemberCtrl(PersistentController):
    @staticmethod
    def create(db: Session, session_id: str, user_id: str, is_admin: bool = False) -> StudySessionMember:
        new_member = StudySessionMember(session_id=session_id, user_id=user_id, is_admin=is_admin)
        db.add(new_member)
        db.commit()
        db.refresh(new_member)
        return new_member

    @staticmethod
    def save(record: StudySessionMember, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> StudySessionMember | None:
        return storage.query(StudySessionMember).filter(StudySessionMember.member_id == identifier, StudySessionMember.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[StudySessionMember]:
        return storage.query(StudySessionMember).filter(*criteria, StudySessionMember.deleted.is_(False)).all()

    @staticmethod
    def safe_delete(record: StudySessionMember, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: StudySessionMember, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
