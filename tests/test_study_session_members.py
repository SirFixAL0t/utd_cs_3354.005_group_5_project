from sqlalchemy.orm import Session
import pytest

from src.classes.study_session import StudySession
from src.controllers.study_sessions import StudySessionCtrl
from src.controllers.study_session_members import StudySessionMemberCtrl
from src.controllers.users import UserCtrl
from src.classes.user import User


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email="ssm-test@example.com",
        pw="password123",
        timezone="UTC",
    )

@pytest.fixture
def another_test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Another Test User",
        email="ssm-test2@example.com",
        pw="password123",
        timezone="UTC",
    )

@pytest.fixture
def test_session(db_session: Session, test_user: User) -> StudySession:
    return StudySessionCtrl.create(
        db=db_session, title="Midterm Review", owner_id=test_user.user_id
    )


def test_study_session_member_creation(db_session: Session, test_session: StudySession, test_user: User):
    """Black-box test for study session member creation."""
    member = StudySessionMemberCtrl.create(
        db=db_session, session_id=test_session.session_id, user_id=test_user.user_id
    )
    assert member.member_id
    assert member.session_id == test_session.session_id
    assert member.user_id == test_user.user_id
    assert not member.is_admin
    assert not member.deleted


def test_study_session_admin_creation(db_session: Session, test_session: StudySession, another_test_user: User):
    """Test creating a study session member with admin privileges."""
    admin_member = StudySessionMemberCtrl.create(
        db=db_session,
        session_id=test_session.session_id,
        user_id=another_test_user.user_id,
        is_admin=True,
    )
    assert admin_member.is_admin
