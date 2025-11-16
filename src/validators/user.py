from src.interfaces import Validator
from src.classes.user import User
from src.constants import DISPLAY_NAME, EMAIL_LENGTH, PASSWORD_LENGTH


class UserValidator(Validator):
    def validate(self, user: User) -> bool:

        if not isinstance(user, User):
            raise TypeError("Object must be of type User")

        if not user.name or len(user.name.strip()) < DISPLAY_NAME[0]:
            raise ValueError(f"User name must be at least {DISPLAY_NAME[0]} character.")

        if len(user.name) > DISPLAY_NAME[1]:
            raise ValueError(f"User name cannot exceed {DISPLAY_NAME[1]} characters.")

        if not user.email or "@" not in user.email or len(user.email) > EMAIL_LENGTH[1]:
            raise ValueError("Invalid email address provided.")

        if len(user.hashed_password) < PASSWORD_LENGTH[0] or len(user.hashed_password) > PASSWORD_LENGTH[1]:
            raise ValueError(
                f"Password must be between {PASSWORD_LENGTH[0]} and {PASSWORD_LENGTH[1]} characters."
            )

        return True
