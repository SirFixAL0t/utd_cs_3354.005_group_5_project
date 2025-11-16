from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.models.event import Event, EventCreate, EventUpdate
from src.models.notification import Notification, NotificationCreate
from src.database import get_db
from src.classes.event import Event as DBEvent
from src.classes.notification import Notification as DBNotification
from src.classes.calendar import Calendar as DBCalendar
from src.classes.user import User as DBUser
from src.api.authorization import get_current_user

router = APIRouter()

@router.post("/events", response_model=Event)
async def create_event(event: EventCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    # For simplicity, we'll use the user's first calendar.
    # In the real application, the user would specify the calendar.
    calendar = db.query(DBCalendar).filter(DBCalendar.user_id == current_user.user_id).first()
    if not calendar:
        calendar = DBCalendar(user_id=current_user.user_id, name="Default Calendar")
        db.add(calendar)
        db.commit()
        db.refresh(calendar)

    db_event = DBEvent(**event.model_dump(), calendar_id=calendar.calendar_id)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/events/{event_id}", response_model=Event)
async def get_event(event_id: str, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    db_event = db.query(DBEvent).join(DBCalendar).filter(DBEvent.event_id == event_id, DBCalendar.user_id == current_user.user_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return db_event

@router.put("/events/{event_id}", response_model=Event)
async def update_event(event_id: str, event: EventUpdate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    db_event = db.query(DBEvent).join(DBCalendar).filter(DBEvent.event_id == event_id, DBCalendar.user_id == current_user.user_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    for key, value in event.model_dump(exclude_unset=True).items():
        setattr(db_event, key, value)
        
    db.commit()
    db.refresh(db_event)
    return db_event

@router.post("/events/{event_id}/notifications", response_model=Notification)
async def add_notification_to_event(event_id: str, notification: NotificationCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    db_event = db.query(DBEvent).join(DBCalendar).filter(DBEvent.event_id == event_id, DBCalendar.user_id == current_user.user_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    
    db_notification = DBNotification(**notification.model_dump(), event_id=event_id)
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification
