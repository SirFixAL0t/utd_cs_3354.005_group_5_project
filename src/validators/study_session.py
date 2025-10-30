from src.interfaces import Validator
from src.classes.study_session import StudySession


class StudySessionValidator(Validator):
    def validate(self, session: StudySession) -> bool:
        if not isinstance(session, StudySession):
            raise TypeError("Object must be of type StudySession")
        if not session.title or len(session.title.strip()) == 0:
            raise ValueError("Study session title cannot be empty.")
        return True
