from typing import Protocol, Any

class Validator(Protocol):
    """
    A protocol for classes that can validate a data object.
    """
    @staticmethod
    def validate(entity: Any) -> bool:
        """
        Validates the given data object.
        
        :param entity: The object to validate.
        :return: True if the object is valid, False otherwise.
        """
        # ... or pass defines no function body for the method in python.
        # This means each validator will have to implement its own from scratch
        ...


class PersistentController(Protocol):
    """
    A protocol for controllers that use database for persistence, and retrieval
    """
    @staticmethod
    def save(record: Any, storage: Any) -> bool:
        """
        Stores the given record in the given storage.
        :param record: The instance to store
        :param storage: The storage instance to use
        """
        ...

    @staticmethod
    def load(identifier: Any, storage: Any) -> Any:
        """
        Load the given identifier from the storage
        :param identifier: The identifier to find
        :param storage: The database to find the record in
        :return:
        """
        ...

    @staticmethod
    def search(criteria: list[Any], storage: Any) -> list[Any]:
        """
        Find any matching records in the storage
        :param criteria: A list of criteria to search for
        :param storage: The database to search into
        :return:
        """

    @staticmethod
    def safe_delete(record: Any, storage: Any) -> bool:
        """
        A virtual delete to mark the record as deleted instead of deleting it from the storage
        :param record: The record to delete
        :param storage: The storage to save the state to
        :return: True if the record was deleted, False otherwise
        """
        ...

    @staticmethod
    def permanent_delete(record: Any, storage: Any) -> bool:
        """
        Delete the record from the database, can't be rolled back
        :param record: The record to delete
        :param storage: The storage to save the state to
        :return: True if the record was deleted, False otherwise
        """