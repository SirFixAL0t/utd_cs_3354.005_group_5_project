from sqlalchemy.orm import declarative_base
import uuid


Base = declarative_base()

def default_uuid():
    return str(uuid.uuid4())
