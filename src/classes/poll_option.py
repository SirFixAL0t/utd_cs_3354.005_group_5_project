from sqlalchemy import Column, String, Boolean, ForeignKey, event
from sqlalchemy.orm import relationship

from src.base_class import Base, default_uuid


class PollOption(Base):
    __tablename__ = 'poll_options'
    option_id = Column(String, primary_key=True, default=default_uuid)
    poll_id = Column(String, ForeignKey('polls.poll_id'), nullable=False)
    option_text = Column(String, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)

    poll = relationship("Poll", back_populates="options")
    votes = relationship("Vote", back_populates="selected_option", cascade="all, delete-orphan")


@event.listens_for(PollOption, 'before_insert')
@event.listens_for(PollOption, 'before_update')
def validate_poll_option(mapper, connection, target):
    from src.validators.poll_option import PollOptionValidator
    PollOptionValidator().validate(target)
