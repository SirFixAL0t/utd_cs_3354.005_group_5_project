# @TODO - auth system should handle the sessions once the UI is connected to the backend
from dataclasses import dataclass
from src.classes.user import User


@dataclass
class AuthSystem:
      registered_users: dict[str, User]
      logged_in_users: dict[str, User]

      def register_user(self, user: User) -> str:
          if user.email in self.registered_users:
              return "User already exists"
          self.registered_users[user.email] = user
          return "Registration successful"


class AuthCtrl:
    @staticmethod
    def create() -> AuthSystem:
        """
        Factory to create an AuthSystem
        :return: a new AuthSystem object
        """
        return AuthSystem(registered_users={}, logged_in_users={})
