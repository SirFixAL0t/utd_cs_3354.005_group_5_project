from typing import Any

from src.interfaces import PersistentController


class ScheduleCtrl(PersistentController):
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
