from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, JSON, event
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime, timezone
import uuid
from src.enums import TaskStatus

Base = declarative_base()

def default_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    pw = Column(String, nullable=False)
    timezone = Column(String)
    calendars = relationship("Calendar", back_populates="user")
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(User, 'before_insert')
@event.listens_for(User, 'before_update')
def validate_user(mapper, connection, target):
    from src.validators.user import UserValidator
    UserValidator().validate(target)

class Event(Base):
    __tablename__ = 'events'
    event_id = Column(String, primary_key=True, default=default_uuid)
    title = Column(String, nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    location = Column(String)
    calendar_id = Column(String, ForeignKey('calendars.calendar_id'))
    calendar = relationship("Calendar", back_populates="events")
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Event, 'before_insert')
@event.listens_for(Event, 'before_update')
def validate_event(mapper, connection, target):
    from src.validators.event import EventValidator
    EventValidator().validate(target)

class Calendar(Base):
    __tablename__ = 'calendars'
    calendar_id = Column(String, primary_key=True, default=default_uuid)
    name = Column(String, nullable=False)
    type = Column(String)
    visibility = Column(String)
    color = Column(String)
    shared = Column(Boolean, default=False)
    events = relationship("Event", back_populates="calendar")
    user_id = Column(String, ForeignKey('users.user_id'))
    user = relationship("User", back_populates="calendars")
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Calendar, 'before_insert')
@event.listens_for(Calendar, 'before_update')
def validate_calendar(mapper, connection, target):
    from src.validators.calendar import CalendarValidator
    CalendarValidator().validate(target)

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

class Notification(Base):
    __tablename__ = 'notifications'
    notification_id = Column(String, primary_key=True, default=default_uuid)
    _type = Column(String)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.now(timezone.utc))
    delivery_status = Column(String)
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Notification, 'before_insert')
@event.listens_for(Notification, 'before_update')
def validate_notification(mapper, connection, target):
    from src.validators.notification import NotificationValidator
    NotificationValidator().validate(target)

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

class ExternalCalendar(Base):
    __tablename__ = 'external_calendars'
    account_id = Column(String, primary_key=True, default=default_uuid)
    provider = Column(String)
    accessToken = Column(String)
    refreshToken = Column(String)
    last_sync = Column(DateTime)
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(ExternalCalendar, 'before_insert')
@event.listens_for(ExternalCalendar, 'before_update')
def validate_external_calendar(mapper, connection, target):
    from src.validators.calendar import ExternalCalendarValidator
    ExternalCalendarValidator().validate(target)

class Task(Base):
    __tablename__ = 'tasks'
    task_id = Column(String, primary_key=True, default=default_uuid)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime)
    status = Column(String, default=TaskStatus.CREATED)
    deleted = Column(Boolean, default=False, nullable=False)

@event.listens_for(Task, 'before_insert')
@event.listens_for(Task, 'before_update')
def validate_task(mapper, connection, target):
    from src.validators.task import TaskValidator
    TaskValidator().validate(target)
