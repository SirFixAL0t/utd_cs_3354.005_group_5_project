from typing import Any
from sqlalchemy.orm import Session

from src.classes.user import User
from src.interfaces import PersistentController


class UserCtrl(PersistentController):
    @staticmethod
    def create(
        db: Session,
        name: str,
        email: str,
        pw: str,
        timezone: str,
    ) -> User:
        """
        Factory to create a User
        :param db: The database session
        :param name: The name of the user
        :param email: The email of the user
        :param pw: The password of the user
        :param timezone: The timezone of the user
        :return: a new User object
        """
        new_user = User(name=name, email=email, pw=pw, timezone=timezone)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    @staticmethod
    def save(record: User, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> User | None:
        return storage.query(User).filter(User.user_id == identifier, User.deleted == False).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[type[User]]:
        # This is a simple search, can be expanded
        return storage.query(User).filter(*criteria, User.deleted==False).all()

    @staticmethod
    def safe_delete(record: User, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: User, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
