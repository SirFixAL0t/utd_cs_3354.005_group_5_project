from sqlalchemy import Column, String, DateTime
from src.base_class import Base
from datetime import datetime

class _SeedLog(Base):
    __tablename__ = '_seed_log'
    filename = Column(String, primary_key=True)
    seeded_at = Column(DateTime, default=datetime.utcnow)
