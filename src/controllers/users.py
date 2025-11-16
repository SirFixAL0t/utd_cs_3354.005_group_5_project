from typing import Any

from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.classes.user import User
from src.interfaces import PersistentController
from src.core.security import get_password_hash
from src.constants import PASSWORD_LENGTH


class UserCtrl(PersistentController):
    @staticmethod
    def create(
        db: Session,
        name: str,
        email: EmailStr,
        password: str,
        timezone: str,
    ) -> User:
        """
        Factory to create a User. Hashes the password before storage.
        :param db: The database session
        :param name: The name of the user
        :param email: The email of the user
        :param password: The plain-text password of the user
        :param timezone: The timezone of the user
        :return: a new User object
        """
        if not (PASSWORD_LENGTH[0] <= len(password) <= PASSWORD_LENGTH[1]):
            raise ValueError("Password length is not valid")
        hashed_password = get_password_hash(password)
        new_user = User(name=name, email=str(email), hashed_password=hashed_password, timezone=timezone)
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
        return storage.query(User).filter(User.user_id == identifier, User.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[type[User]]:
        return storage.query(User).filter(*criteria, User.deleted.is_(False)).all()

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
