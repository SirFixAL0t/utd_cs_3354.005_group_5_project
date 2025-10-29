from typing import Any

from src.classes import Friend
from src.interfaces import PersistentController


class FriendsCtrl(PersistentController):
    @staticmethod
    def create(
        left_id: str,
        right_id: str,
        status: str,
        nickname: str,
    ) -> Friend:
        """
        Factory to create a Friend
        :param left_id: The ID of the first user in the friendship
        :param right_id: The ID of the second user in the friendship
        :param status: The status of the friendship
        :param nickname: The nickname for the friend
        :return: a new Friend object
        """
        return Friend(
            left_id=left_id,
            right_id=right_id,
            status=status,
            nickname=nickname,
        )

    @staticmethod
    def save(record: Any, storage: Any) -> bool:
        # @TODO implement method
        pass

    @staticmethod
    def load(identifier: Any, storage: Any) -> Any:
        # @TODO implement method
        pass

    @staticmethod
    def search(criteria: list[Any], storage: Any) -> list[Any]:
        # @TODO implement method
        pass

    @staticmethod
    def safe_delete(record: Any, storage: Any) -> bool:
        # @TODO implement method
        pass

    @staticmethod
    def permanent_delete(record: Any, storage: Any) -> bool:
        # @TODO implement method
        pass
