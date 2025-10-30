from sqlalchemy import Column, String, Boolean, JSON, event
from src.base_class import Base, default_uuid


class Poll(Base):
    __tablename__ = 'polls'
    poll_id = Column(String, primary_key=True, default=default_uuid)
    question = Column(String, nullable=False)
    options = Column(JSON, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Poll, 'before_insert')
@event.listens_for(Poll, 'before_update')
def validate_poll(mapper, connection, target):
    from src.validators.poll import PollValidator
    PollValidator().validate(target)
