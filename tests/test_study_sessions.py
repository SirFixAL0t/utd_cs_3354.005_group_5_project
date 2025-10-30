from sqlalchemy.orm import Session
import pytest

from src.classes.study_session import StudySession
from src.controllers.study_sessions import StudySessionCtrl
from src.controllers.users import UserCtrl
from src.classes.user import User
from src.enums import SessionStatus
from src.constants import CALENDAR_TITLE


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email="ss-test@example.com",
        pw="password123",
        timezone="UTC",
    )


def test_study_session_creation(db_session: Session, test_user: User):
    """Black-box test for study session creation."""
    session = StudySessionCtrl.create(
        db=db_session, title="Midterm Review", owner_id=test_user.user_id
    )
    assert session.session_id
    assert session.title == "Midterm Review"
    assert session.status == SessionStatus.ACTIVE
    assert not session.deleted


def test_study_session_creation_no_title(db_session: Session, test_user: User):
    """Boundary test for study session creation with no title."""
    with pytest.raises(ValueError):
        StudySessionCtrl.create(db=db_session, title="", owner_id=test_user.user_id)


def test_study_session_creation_long_title(db_session: Session, test_user: User):
    """Boundary test for study session creation with a title that is too long."""
    long_title = "a" * (CALENDAR_TITLE[1] + 1)
    with pytest.raises(ValueError):
        StudySessionCtrl.create(db=db_session, title=long_title, owner_id=test_user.user_id)
