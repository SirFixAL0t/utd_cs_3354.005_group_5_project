from sqlalchemy.orm import Session
import pytest

from src.classes.user import User
from src.controllers.users import UserCtrl


def test_user_creation(db_session: Session):
    """Black-box test for user creation."""
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test@example.com",
        pw="password",
        timezone="UTC",
    )
    assert user.user_id
    assert user.name == "Test User"
    assert not user.deleted


def test_user_creation_empty_name(db_session: Session):
    """Boundary test for user creation with an empty name."""
    with pytest.raises(Exception):
        UserCtrl.create(
            db=db_session,
            name="",
            email="test@example.com",
            pw="password",
            timezone="UTC",
        )


def test_user_creation_invalid_email(db_session: Session):
    """Boundary test for user creation with an invalid email."""
    with pytest.raises(Exception):
        UserCtrl.create(
            db=db_session,
            name="Test User",
            email="invalid-email",
            pw="password",
            timezone="UTC",
        )


def test_user_soft_delete(db_session: Session):
    """White-box test for user soft delete."""
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test@example.com",
        pw="password",
        timezone="UTC",
    )
    UserCtrl.safe_delete(user, db_session)
    deleted_user = UserCtrl.load(user.user_id, db_session)
    assert deleted_user is None

    # Verify that the user is still in the database but marked as deleted
    deleted_user_in_db = db_session.query(User).filter(User.user_id == user.user_id).first()
    assert deleted_user_in_db
    assert deleted_user_in_db.deleted


def test_user_permanent_delete(db_session: Session):
    """White-box test for user permanent delete."""
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test@example.com",
        pw="password",
        timezone="UTC",
    )
    UserCtrl.permanent_delete(user, db_session)
    deleted_user = UserCtrl.load(user.user_id, db_session)
    assert deleted_user is None

    # Verify that the user is no longer in the database
    deleted_user_in_db = db_session.query(User).filter(User.user_id == user.user_id).first()
    assert deleted_user_in_db is None
