from src.interfaces import Validator
from src.classes.user import User

class UserValidator(Validator):

    @staticmethod
    def validate(user: User) -> bool:
        if not isinstance(user, User):
            raise TypeError("Object must be of type User")
        if not user.name or len(user.name.strip()) == 0:
            raise ValueError("User name cannot be empty.")
        if len(user.name) > 50:
            raise ValueError("User name cannot exceed 50 characters.")
        if not user.email or '@' not in user.email:
            raise ValueError("Invalid email address provided.")
        return True
