from typing import Any
from sqlalchemy.orm import Session

from src.classes.friend import Friend
from src.interfaces import PersistentController


class FriendsCtrl(PersistentController):
    @staticmethod
    def create(
        db: Session,
        left_id: str,
        right_id: str,
        status: str,
        nickname: str,
    ) -> Friend:
        """
        Factory to create a Friend
        :param db: The database session
        :param left_id: The ID of the first user in the friendship
        :param right_id: The ID of the second user in the friendship
        :param status: The status of the friendship
        :param nickname: The nickname for the friend
        :return: a new Friend object
        """
        new_friendship = Friend(
            left_id=left_id,
            right_id=right_id,
            status=status,
            nickname=nickname,
        )
        db.add(new_friendship)
        db.commit()
        db.refresh(new_friendship)
        return new_friendship

    @staticmethod
    def save(record: Friend, storage: Session) -> bool:
        storage.add(record)
        storage.commit()
        storage.refresh(record)
        return True

    @staticmethod
    def load(identifier: str, storage: Session) -> Friend | None:
        return storage.query(Friend).filter(Friend.friendship_id == identifier, Friend.deleted.is_(False)).first()

    @staticmethod
    def search(criteria: list[Any], storage: Session) -> list[Friend]:
        return storage.query(Friend).filter(*criteria, Friend.deleted.is_(False)).all()

    @staticmethod
    def safe_delete(record: Friend, storage: Session) -> bool:
        record.deleted = True
        storage.commit()
        return True

    @staticmethod
    def permanent_delete(record: Friend, storage: Session) -> bool:
        storage.delete(record)
        storage.commit()
        return True
