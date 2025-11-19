from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import List
from src.models.event import Event, EventCreate, EventUpdate
from src.models.notification import Notification, NotificationCreate
from src.models.calendar import Calendar
from src.database import get_db
from src.classes.event import Event as DBEvent
from src.classes.notification import Notification as DBNotification
from src.classes.calendar import Calendar as DBCalendar
from src.classes.user import User as DBUser
from src.api.authorization import get_current_user

router = APIRouter()

@router.get("/", response_model=List[Calendar])
def get_user_calendars(db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    """
    Retrieve all calendars for the currently authenticated user.
    """
    return db.query(DBCalendar).filter(DBCalendar.user_id == current_user.user_id).all()

@router.post("/{calendar_id}/events", response_model=Event)
async def create_event(calendar_id: str, event: EventCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    # Verify the calendar belongs to the current user
    calendar = db.query(DBCalendar).filter(DBCalendar.calendar_id == calendar_id, DBCalendar.user_id == current_user.user_id).first()
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found or you do not have permission to create events in it.")

    db_event = DBEvent(**event.model_dump(), calendar_id=calendar_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/{calendar_id}/events", response_model=List[Event])
def get_calendar_events(calendar_id: str, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    """
    Retrieve all events for a specific calendar owned by the currently authenticated user.
    """
    # First, verify the calendar belongs to the current user
    calendar = db.query(DBCalendar).filter(DBCalendar.calendar_id == calendar_id, DBCalendar.user_id == current_user.user_id).first()
    if not calendar:
        raise HTTPException(status_code=404, detail="Calendar not found or you do not have permission to view it.")
    
    return db.query(DBEvent).filter(DBEvent.calendar_id == calendar_id).all()

#dev testinggggggggggg
@router.get("/events", response_model=List[Event])
def get_user_events(db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    """
    Retrieve all events across all calendars owned by the currently authenticated user.
    """
    return (
        db
        .query(DBEvent)
        .join(DBCalendar)
        .filter(DBCalendar.user_id == current_user.user_id, DBEvent.deleted == False)
        .all()
    )


@router.get("/events/public", response_model=List[Event])
def get_public_events(db: Session = Depends(get_db)):
    """
    Retrieve events from public/shared calendars for unauthenticated access (dev/testing).
    """
    return (
        db
        .query(DBEvent)
        .join(DBCalendar)
        .filter(or_(DBCalendar.visibility == 'public', DBCalendar.shared == True), DBEvent.deleted == False, DBCalendar.deleted == False)
        .all()
    )

@router.get("/{calendar_id}/events/{event_id}", response_model=Event)
async def get_event(calendar_id: str, event_id: str, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    db_event = db.query(DBEvent).join(DBCalendar).filter(
        DBEvent.event_id == event_id,
        DBCalendar.calendar_id == calendar_id,
        DBCalendar.user_id == current_user.user_id
    ).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.put("/{calendar_id}/events/{event_id}", response_model=Event)
async def update_event(calendar_id: str, event_id: str, event: EventUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    db_event = db.query(DBEvent).join(DBCalendar).filter(
        DBEvent.event_id == event_id,
        DBCalendar.calendar_id == calendar_id,
        DBCalendar.user_id == current_user.user_id
    ).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.model_dump(exclude_unset=True).items():
        setattr(db_event, key, value)
        
    db.commit()
    db.refresh(db_event)
    return db_event

@router.post("/{calendar_id}/events/{event_id}/notifications", response_model=Notification)
async def add_notification_to_event(
        calendar_id: str,
        event_id: str,
        notification: NotificationCreate,
        db: Session = Depends(get_db),
        current_user: DBUser = Depends(get_current_user)):
    db_event = (db
                .query(DBEvent)
                .join(DBCalendar)
                .filter(
        DBEvent.event_id == event_id,
        DBCalendar.user_id == current_user.user_id,
        DBEvent.calendar_id == calendar_id).first())
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_notification = DBNotification(**notification.model_dump(), event_id=event_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
