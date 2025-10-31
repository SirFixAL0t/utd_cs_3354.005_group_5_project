from src.classes.friend import Friend
from src.interfaces import Validator
from src.constants import DISPLAY_NAME


class FriendValidator(Validator):
    def validate(self, friend: Friend) -> bool:
        if not isinstance(friend, Friend):
            raise TypeError("Object must be of type Friend")

        if friend.left_id == friend.right_id:
            raise ValueError("A user cannot be friends with themselves.")

        if friend.nickname and len(friend.nickname) > DISPLAY_NAME[1]:
            raise ValueError(f"Nickname cannot exceed {DISPLAY_NAME[1]} characters.")

        return True
