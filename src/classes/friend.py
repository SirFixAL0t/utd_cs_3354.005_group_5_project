from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON, event
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid


class Friend(Base):
    __tablename__ = 'friends'
    friendship_id = Column(String, primary_key=True, default=default_uuid)
    left_id = Column(String, ForeignKey('users.user_id'))
    right_id = Column(String, ForeignKey('users.user_id'))
    status = Column(String)
    nickname = Column(String)
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Friend, 'before_insert')
@event.listens_for(Friend, 'before_update')
def validate_friend(mapper, connection, target):
    from src.validators.friend import FriendValidator
    FriendValidator().validate(target)
