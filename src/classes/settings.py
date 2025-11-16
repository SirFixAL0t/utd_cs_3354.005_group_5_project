from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from src.base_class import Base, default_uuid

class Settings(Base):
    __tablename__ = 'settings'
    settings_id = Column(String, primary_key=True, default=default_uuid)
    theme = Column(String, nullable=False, default="dark")
    timezone = Column(String, nullable=False, default="UTC")
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False, unique=True)

    user = relationship("User")

# @TODO Add validation for settings and run it here
