from src.interfaces import Validator
from src.classes.study_session import StudySession
from src.constants import CALENDAR_TITLE


class StudySessionValidator(Validator):
    def validate(self, session: StudySession) -> bool:
        if not isinstance(session, StudySession):
            raise TypeError("Object must be of type StudySession")

        if not session.title or len(session.title.strip()) < CALENDAR_TITLE[0]:
            raise ValueError(f"Study session title must be at least {CALENDAR_TITLE[0]} character.")
        if len(session.title) > CALENDAR_TITLE[1]:
            raise ValueError(f"Study session title cannot exceed {CALENDAR_TITLE[1]} characters.")

        return True
