from fastapi import APIRouter
from src.api import authorization, calendar, settings, polls

"""
Container for all routing capabilities of the backend's API.
This will be loaded in the main.py entry point
"""

api_router = APIRouter()

api_router.include_router(authorization.router, prefix="/auth", tags=["auth"])
api_router.include_router(calendar.router, prefix="/calendar", tags=["calendar"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(polls.router, prefix="/polls", tags=["polls"])
