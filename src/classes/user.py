from sqlalchemy import Column, String, Boolean, event
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    timezone = Column(String)
    deleted = Column(Boolean, default=False, nullable=False)

    calendars = relationship("Calendar", back_populates="user")
    session_memberships = relationship("StudySessionMember", back_populates="user")
    votes = relationship("Vote", back_populates="voter")
    # Relationships for Friend model
    friendships_left = relationship("Friend", foreign_keys="[Friend.left_id]", back_populates="left_user")
    friendships_right = relationship("Friend", foreign_keys="[Friend.right_id]", back_populates="right_user")


@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def validate_user(mapper, connection, target):
    from src.validators.user import UserValidator
    UserValidator().validate(target)
