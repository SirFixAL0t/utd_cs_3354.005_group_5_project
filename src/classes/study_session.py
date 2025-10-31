from sqlalchemy import Column, String, Boolean, ForeignKey, event, Enum
from sqlalchemy.orm import relationship

from src.base_class import Base, default_uuid
from src.enums import SessionStatus


class StudySession(Base):
    __tablename__ = 'study_sessions'
    session_id = Column(String, primary_key=True, default=default_uuid)
    title = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    status = Column(Enum(SessionStatus), nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    owner = relationship("User")
    members = relationship("StudySessionMember", back_populates="session", cascade="all, delete-orphan")


@event.listens_for(StudySession, 'before_insert')
@event.listens_for(StudySession, 'before_update')
def validate_study_session(mapper, connection, target):
    from src.validators.study_session import StudySessionValidator
    StudySessionValidator().validate(target)
