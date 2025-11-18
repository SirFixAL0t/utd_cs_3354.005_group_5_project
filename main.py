from fastapi import FastAPI
from src.api.api_router import api_router
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Get the frontend origin from an environment variable
# Default to http://localhost:3000 for local development
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")

origins = [
    frontend_origin,
]

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
