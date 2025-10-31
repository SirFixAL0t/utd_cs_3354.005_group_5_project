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

      def login(self, email: str, password: str) -> str:
          if email not in self.registered_users:
              return "User not found"
          user = self.registered_users[email]
          if user.pw != password:
              return "Incorrect password"
          self.logged_in_users[email] = user
          return "Login successful"

      def logout(self, email: str) -> str:
          if email not in self.logged_in_users:
              return "User not logged in"
          del self.logged_in_users[email]
          return "Logout successful"


class AuthCtrl:
    @staticmethod
    def create() -> AuthSystem:
        """
        Factory to create an AuthSystem
        :return: a new AuthSystem object
        """
        return AuthSystem(registered_users={}, logged_in_users={})
