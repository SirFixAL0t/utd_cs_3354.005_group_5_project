from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.models.settings import Settings, SettingsCreate
from src.database import get_db
from src.classes.settings import Settings as DBSettings
from src.classes.user import User as DBUser
from src.api.authorization import get_current_user

router = APIRouter()

@router.get("/", response_model=Settings)
async def read_settings(db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    # @TODO - Create a non-safe read_settings that does not create the settings if not found and instead
    # it raises an exception
    settings = db.query(DBSettings).filter(DBSettings.user_id == current_user.user_id).first()
    if not settings:
        settings = DBSettings(user_id=current_user.user_id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/", response_model=Settings)
async def update_settings(settings_update: SettingsCreate, db: Session = Depends(get_db), current_user: DBUser = Depends(get_current_user)):
    # @TODO Make a helper function to return settings = db.query(...)
    #  or create a new setting for that user if it doesn't exist - to simplify this function
    settings = db.query(DBSettings).filter(DBSettings.user_id == current_user.user_id).first()
    if not settings:
        settings = DBSettings(user_id=current_user.user_id, **settings_update.model_dump())
        db.add(settings)
    else:
        for key, value in settings_update.model_dump().items():
            setattr(settings, key, value)
    db.commit()
    db.refresh(settings)
    return settings
