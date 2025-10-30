from src.classes import Friend
from src.interfaces import Validator


class FriendValidator(Validator):

    @staticmethod
    def validate(friend: Friend) -> bool:
        if not isinstance(friend, Friend):
            raise TypeError("Object must be of type Friend")
        if friend.left_id == friend.right_id:
            raise ValueError("A user cannot be friends with themselves.")
        return True