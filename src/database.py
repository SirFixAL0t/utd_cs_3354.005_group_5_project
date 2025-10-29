from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# In a real application, this would come from a config file
DATABASE_URL = "sqlite:///:memory:"  # Using in-memory SQLite for now

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
