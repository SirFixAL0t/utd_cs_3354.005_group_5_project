import os
import json
import argparse
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import all classes that have relationships to ensure SQLAlchemy can resolve them
from src.classes.user import User
from src.classes.calendar import Calendar
from src.classes.event import Event
from src.classes.seed_log import _SeedLog
from src.classes.friend import Friend
from src.classes.notification import Notification
from src.classes.poll import Poll
from src.classes.poll_option import PollOption
from src.classes.study_session import StudySession
from src.classes.study_session_member import StudySessionMember
from src.classes.vote import Vote

from src.controllers.users import UserCtrl
from src.controllers.calendar import CalendarCtrl
from src.controllers.events import EventCtrl
from src.base_class import Base
from src.core.config import DATABASE_URL

def seed_users(session, data):
    for user_data in data:
        user = UserCtrl.create(
            db=session,
            name=user_data["name"],
            email=user_data["email"],
            password=user_data["password"],
            timezone=user_data["timezone"],
        )
        user.is_seeded = True
    session.commit()

def seed_calendars(session, data):
    for cal_data in data:
        user = session.query(User).filter(User.email == cal_data["user_email"]).first()
        if not user:
            print(f"Warning: User with email {cal_data['user_email']} not found. Skipping calendar '{cal_data['name']}'.")
            continue
        if not 'shared' in cal_data or cal_data['shared'] is None:
            cal_data['shared'] = False
        calendar = CalendarCtrl.create(
            db=session,
            name=cal_data["name"],
            calendar_type=cal_data["calendar_type"],
            visibility=cal_data["visibility"],
            color=cal_data["color"],
            shared=cal_data['shared'],
            user_id=user.user_id
        )
        calendar.code = cal_data["code"] # Manually set the code for predictable seeds
        calendar.is_seeded = True
    session.commit()

def seed_events(session, data):
    for event_data in data:
        user = session.query(User).filter(User.email == event_data["user_email"]).first()
        if not user:
            print(f"Warning: User with email {event_data['user_email']} not found. Skipping event '{event_data['title']}'.")
            continue

        calendar = session.query(Calendar).filter(
            Calendar.user_id == user.user_id,
            Calendar.code == event_data["calendar_code"]
        ).first()

        if not calendar:
            print(f"Warning: Calendar with code '{event_data['calendar_code']}' for user '{event_data['user_email']}' not found. Skipping event '{event_data['title']}'.")
            continue

        # Convert ISO 8601 string to datetime object
        start_time = datetime.fromisoformat(event_data["start_time"].replace('Z', '+00:00'))
        end_time = datetime.fromisoformat(event_data["end_time"].replace('Z', '+00:00'))

        event = EventCtrl.create(
            db=session,
            title=event_data["title"],
            start_time=start_time,
            end_time=end_time,
            location=event_data["location"],
            calendar_id=calendar.calendar_id
        )
        event.is_seeded = True
    session.commit()

def seed_database(force=False):
    """
    Seeds the database with data from the seeds/ directory.
    """
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    if force:
        print("Force option detected. Removing previously seeded data...")
        session.query(Event).filter(Event.is_seeded == True).delete()
        session.query(Calendar).filter(Calendar.is_seeded == True).delete()
        session.query(User).filter(User.is_seeded == True).delete()
        session.query(_SeedLog).delete()
        session.commit()
        print("Seeded data removed.")

    seed_dir = "seeds"
    # Ensure users are seeded first, then calendars, then events
    seed_order = ["users.json", "calendars.json", "events.json"]
    
    for filename in seed_order:
        filepath = os.path.join(seed_dir, filename)
        if not os.path.exists(filepath):
            continue

        if session.query(_SeedLog).filter(_SeedLog.filename == filename).first():
            print(f"Skipping already run seed: {filename}")
            continue

        print(f"Running seed: {filename}")
        with open(filepath, 'r') as f:
            data = json.load(f)
            
            if "users" in filename:
                seed_users(session, data)
            elif "calendars" in filename:
                seed_calendars(session, data)
            elif "events" in filename:
                seed_events(session, data)

        session.add(_SeedLog(filename=filename))
        session.commit()
        print(f"Finished seed: {filename}")

    session.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed the database with initial data.")
    parser.add_argument("--force", action="store_true", help="Remove all seeded data and re-seed.")
    args = parser.parse_args()
    
    seed_database(force=args.force)
