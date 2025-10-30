from typing import Any

from src.classes import Poll
from src.interfaces import PersistentController


class PollCtrl(PersistentController):
    @staticmethod
    def create(question: str, options: list[str]) -> Poll:
        """
        Factory to create a Poll
        :param question: The question for the poll
        :param options: The options for the poll
        :return: a new Poll object
        """
        return Poll(question=question, options=options)

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
