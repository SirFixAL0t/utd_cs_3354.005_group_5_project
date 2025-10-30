from sqlalchemy.orm import Session
import pytest

from src.classes.study_session import StudySession
from src.controllers.study_sessions import StudySessionCtrl
from src.controllers.users import UserCtrl
from src.classes.user import User


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test@example.com",
        pw="password",
        timezone="UTC",
    )


def test_study_session_creation(db_session: Session, test_user: User):
    """Black-box test for study session creation."""
    session = StudySessionCtrl.create(
        db=db_session, title="Midterm Review", owner_id=test_user.user_id
    )
    assert session.session_id
    assert session.title == "Midterm Review"
    assert not session.deleted


def test_study_session_creation_no_title(db_session: Session, test_user: User):
    """Boundary test for study session creation with no title."""
    with pytest.raises(ValueError):
        StudySessionCtrl.create(db=db_session, title="", owner_id=test_user.user_id)
