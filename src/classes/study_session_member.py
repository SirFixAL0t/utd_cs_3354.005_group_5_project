from sqlalchemy import Column, String, Boolean, ForeignKey, event
from sqlalchemy.orm import relationship

from src.base_class import Base, default_uuid


class StudySessionMember(Base):
    __tablename__ = 'study_session_members'
    member_id = Column(String, primary_key=True, default=default_uuid)
    session_id = Column(String, ForeignKey('study_sessions.session_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    is_admin = Column(Boolean, default=False, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    session = relationship("StudySession", back_populates="members")
    user = relationship("User")


@event.listens_for(StudySessionMember, 'before_insert')
@event.listens_for(StudySessionMember, 'before_update')
def validate_study_session_member(mapper, connection, target):
    from src.validators.study_session_member import StudySessionMemberValidator
    StudySessionMemberValidator().validate(target)
