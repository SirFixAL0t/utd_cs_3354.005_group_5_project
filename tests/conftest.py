import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# Add the src directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.base_class import Base
from main import app
from src.database import get_db


@pytest.fixture(scope="session")
def engine():
    # Without check_same_thread sqlite complains and fails the tests because of same thread operations
    # This should be alright for our purposes, so it is skipped for now
    return create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})


@pytest.fixture(scope="session")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything."""
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session # Give control back to the caller. When control is returned, the remainder of the code will be run

    session.close()
    # roll back the broader transaction, if it's still active
    if transaction.is_active:
        transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture
def client(db_session):
    """Returns a FastAPI test client with the database dependency overridden."""
    # This may raise some concerns on the IDE level saying dependency_overrides do not exist in fastAPI
    # If it does, ignore it or hide those errors - it does exist but it seems to be a dynamic field
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c # Yield control to the caller until it is done, then remove the overrides for next test
    app.dependency_overrides.clear()
