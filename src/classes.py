from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class User:
    user_id: str
    name: str
    email: str
    pw: str
    timezone: str
    calendars: list[str]

    def change_password(self, new_pw: str):
        self.pw = new_pw

    def set_timezone(self, timezone: str):
        self.timezone = timezone

    def get_timezone(self):
        return self.timezone

    def set_name(self, name: str):
        self.name = name

    def __repr__(self):
        return {
            "id": self.user_id,
            "name": self.name,
            "email": self.email,
            "timezone": self.timezone
        }

    def add_calendar(self, calendar: str):
        self.calendars.append(calendar)


@dataclass
class Event:
    event_id: str
    title: str
    start_time: datetime
    end_time: datetime
    location: str

    def set_start_time(self, start_time: datetime):
        self.start_time = start_time

    def set_end_time(self, end_time: datetime):
        self.end_time = end_time

    def update_event(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_event(self) -> dict[str, str|datetime]:
        return {
            "event_id": self.event_id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location
        }


@dataclass
class Calendar:
    calendar_id: str
    name: str
    type: str
    visibility: str
    color: str
    shared: bool
    events: list[Event]

    def create_event(self, event: Event):
        self.events.append(event)

    def edit_event(self, event_id: str, **kwargs):
        for e in self.events:
            if e.event_id == event_id:
                e.update_event(**kwargs)
                return f"Event {event_id} updated"
        return "Event not found"

    def delete_event(self, event_id: str):
        original_count = len(self.events)
        self.events = [e for e in self.events if e.event_id != event_id]
        return "Event deleted" if len(self.events) < original_count else "Event not found"

    def share_calendar(self, status: bool = True):
        self.shared = status

    def is_shared(self):
        return self.shared

    def get_calendar(self):
        return {
            "calendar_id": self.calendar_id,
            "name": self.name,
            "type": self.type,
            "visibility": self.visibility,
            "color": self.color,
            "shared": self.shared,
            "events": [e.get_event() for e in self.events]
        }

@dataclass
class SharedCalendar(Calendar):
    permission_level: int
    shared_id: int

@dataclass
class AuthSystem:
    registered_users: dict[str, User]
    logged_in_users: dict[str, User]

    def register_user(self, user: User) -> str:
        if user.email in self.registered_users:
            return "User already exists"
        self.registered_users[user.email] = user
        return "Registration successful"

    def login(self, email: str, password: str) -> str:
        user = self.registered_users.get(email)
        if not user:
            return "No user found"
        # @TODO - use crypto in the later versions
        if user.pw != password:
            return "Incorrect password"
        self.logged_in_users[user.email] = user
        return f"Logged in as {user.name}"

    def logout(self, email: str):
        if len(self.logged_in_users.keys()) == 0 or email not in self.logged_in_users:
            return "User is not logged in"

        user_record = self.logged_in_users.get(email)
        self.logged_in_users.pop(email) # remove it from the list.

        return f"{user_record.name} logged out"

@dataclass
class Poll:
    poll_id: str
    question: str
    options: list[str]

@dataclass
class Vote:
    poll_id: int
    user_id: int
    selected_option: str
    timestamp: datetime

@dataclass
class Notifications:
    notification_id: str
    _type: str
    message: str
    timestamp: datetime
    delivery_status: str

@dataclass
class Friend:
    friendship_id: str
    left_id: str
    right_id: str
    status: str
    nickname: str

@dataclass
class ExternalCalendar:
    account_id: str
    provider: str
    accessToken: str
    refreshToken: str
    last_sync: datetime



