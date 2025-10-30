from src.interfaces import Validator
from src.classes.study_session_member import StudySessionMember


class StudySessionMemberValidator(Validator):
    def validate(self, member: StudySessionMember) -> bool:
        if not isinstance(member, StudySessionMember):
            raise TypeError("Object must be of type StudySessionMember")
        # Add more specific validation rules if needed, e.g., user_id and session_id exist
        return True
