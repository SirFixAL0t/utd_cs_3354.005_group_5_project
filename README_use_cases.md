Project Overview

This project is a student calendar and scheduling system. Users can:

Register / Login / Logout

Create calendars and manage them

Create, edit, delete events in calendars

Implemented Classes

User – Manages user info, calendars.

AuthSystem – Handles registration, login, logout.

Calendar – Stores events and supports CRUD operations.

Event – Stores event details and can be updated.

How to Use

Register a user

auth.register_user(user)


Login

auth.login(email, password)


Create calendar

user.add_calendar(calendar)


Add event

calendar.create_event(event)


Edit event

calendar.edit_event(event_id, title="New Title")


Delete event

calendar.delete_event(event_id)


Logout

auth.logout()