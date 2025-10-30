from sqlalchemy import Column, String, Boolean, ForeignKey, event
from sqlalchemy.orm import relationship

from src.base_class import Base, default_uuid


class Poll(Base):
    __tablename__ = 'polls'
    poll_id = Column(String, primary_key=True, default=default_uuid)
    question = Column(String, nullable=False)
    owner_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    options = relationship("PollOption", back_populates="poll", cascade="all, delete-orphan")
    deleted = Column(Boolean, default=False, nullable=False)
    allow_multi_votes = Column(Boolean, default=False)

    owner = relationship("User")


@event.listens_for(Poll, 'before_insert')
@event.listens_for(Poll, 'before_update')
def validate_poll(mapper, connection, target):
    from src.validators.poll import PollValidator
    PollValidator().validate(target)
