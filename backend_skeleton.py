from datetime import datetime

# ---------- USER CLASS ----------
class User:
    def __init__(self, user_id: str, name: str, email: str, pw: str, timezone: str):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.pw = pw
        self.timezone = timezone
        self.calendars = []

    def change_password(self, new_pw: str):
        self.pw = new_pw

    def set_timezone(self, timezone: str):
        self.timezone = timezone

    def get_timezone(self):
        return self.timezone

    def set_name(self, name: str):
        self.name = name

    def get_user(self):
        return {"id": self.user_id, "name": self.name, "email": self.email}

    def add_calendar(self, calendar):
        self.calendars.append(calendar)


# ---------- AUTH SYSTEM ----------
class AuthSystem:
    def __init__(self):
        self.registered_users = {}  # {email: User object}
        self.logged_in_user = None

    def register_user(self, user: User):
        if user.email in self.registered_users:
            return "User already exists"
        self.registered_users[user.email] = user
        return "Registration successful"

    def login(self, email: str, password: str):
        user = self.registered_users.get(email)
        if not user:
            return "No user found"
        if user.pw != password:
            return "Incorrect password"
        self.logged_in_user = user
        return f"Logged in as {user.name}"

    def logout(self):
        if self.logged_in_user:
            name = self.logged_in_user.name
            self.logged_in_user = None
            return f"{name} logged out"
        return "No user is logged in"


# ---------- EVENT CLASS ----------
class Event:
    def __init__(self, event_id: str, title: str, start_time: datetime, end_time: datetime, location: str):
        self.event_id = event_id
        self.title = title
        self.start_time = start_time
        self.end_time = end_time
        self.location = location

    def set_start_time(self, start_time: datetime):
        self.start_time = start_time

    def set_end_time(self, end_time: datetime):
        self.end_time = end_time

    def update_event(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_event(self):
        return {
            "event_id": self.event_id,
            "title": self.title,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location
        }


# ---------- CALENDAR CLASS ----------
class Calendar:
    def __init__(self, calendar_id: str, name: str, type_: str, visibility: str, color: str, shared: bool = False):
        self.calendar_id = calendar_id
        self.name = name
        self.type = type_
        self.visibility = visibility
        self.color = color
        self.shared = shared
        self.events = []

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

    def share_calendar(self):
        self.shared = True

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
