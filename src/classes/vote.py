from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON, event
from src.base_class import Base, default_uuid
from datetime import datetime, timezone


class Vote(Base):
    __tablename__ = 'votes'
    vote_id = Column(String, primary_key=True, default=default_uuid)
    poll_id = Column(String, ForeignKey('polls.poll_id'))
    user_id = Column(String, ForeignKey('users.user_id'))
    selected_option = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Vote, 'before_insert')
@event.listens_for(Vote, 'before_update')
def validate_vote(mapper, connection, target):
    from src.validators.vote import VoteValidator
    VoteValidator().validate(target)
