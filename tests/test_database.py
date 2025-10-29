from sqlalchemy.orm import Session

from src.classes import User
from src.controllers.users import UserCtrl


def test_database_connection(db_session: Session):
    assert db_session


def test_data_storage_and_retrieval(db_session: Session):
    # Create a user
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test@example.com",
        pw="password",
        timezone="UTC",
    )

    # Retrieve the user
    retrieved_user = UserCtrl.load(user.user_id, db_session)

    # Assert that the retrieved user is the same as the created user
    assert retrieved_user.user_id == user.user_id
    assert retrieved_user.name == user.name
    assert retrieved_user.email == user.email
