from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, event
from sqlalchemy.orm import relationship

from src.base_class import Base, default_uuid
from datetime import datetime, timezone


class Vote(Base):
    __tablename__ = 'votes'
    vote_id = Column(String, primary_key=True, default=default_uuid)
    poll_option_id = Column(String, ForeignKey('poll_options.option_id'), nullable=False)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    deleted = Column(Boolean, default=False, nullable=False)

    selected_option_obj = relationship("PollOption", back_populates="votes")
    voter = relationship("User")


@event.listens_for(Vote, 'before_insert')
@event.listens_for(Vote, 'before_update')
def validate_vote(mapper, connection, target):
    from src.validators.vote import VoteValidator
    VoteValidator().validate(target)
