from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.api.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware
import os

# Import all SQLAlchemy models here to ensure they are registered with the Base
from src.classes import (
    user, calendar, event, friend, notification, poll, poll_option, 
    seed_log, settings, study_session, study_session_member, task, vote
)

app = FastAPI()

# Get the frontend origin from an environment variable
# Default to http://localhost:3000 for local development
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

origins = [
    frontend_origin,
]

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"An unexpected error occurred: {exc}"},
    )

app.add_middleware(
    # CORS is needed since the backend and frontend may be in different servers and therefore have different
    # URLS. If the URLs are not in CORS and they differ, the browser is likely going to block that request
    # since it is considered a security risk.
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
