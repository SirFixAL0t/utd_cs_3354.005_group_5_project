from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.core.config import DATABASE_URL

"""# Force using in-memory SQLite for now for tests
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
"""
#need to use the db created from the seeding 
connect_args = {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
