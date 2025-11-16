from sqlalchemy.orm import Session
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
import uuid
from pydantic import EmailStr, TypeAdapter

from src.classes.study_session import StudySession
from src.controllers.study_sessions import StudySessionCtrl
from src.controllers.users import UserCtrl
from src.classes.user import User
from src.enums import SessionStatus
from src.constants import CALENDAR_TITLE

EmailAdapter = TypeAdapter(EmailStr)


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email=EmailAdapter.validate_python(f"ss-test-{uuid.uuid4()}@example.com"),
        password="password123",
        timezone="UTC",
    )


study_session_strategy = st.builds(
    StudySession,
    title=st.text(min_size=CALENDAR_TITLE[0], max_size=CALENDAR_TITLE[1]),
    status=st.sampled_from(SessionStatus),
)

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(session_data=study_session_strategy)
def test_study_session_creation_and_retrieval_property(
    db_session: Session, test_user: User, session_data: StudySession
):
    """Property-based test for study session creation and retrieval."""
    try:
        created_session = StudySessionCtrl.create(
            db=db_session,
            title=session_data.title,
            owner_id=test_user.user_id,
            status=session_data.status,
        )
    except Exception:
        db_session.rollback()
        return

    loaded_session = StudySessionCtrl.load(created_session.session_id, db_session)

    assert loaded_session is not None
    assert loaded_session.title == created_session.title
    assert loaded_session.status == created_session.status


def test_study_session_creation(db_session: Session, test_user: User):
    """Black-box test for study session creation."""
    session = StudySessionCtrl.create(
        db=db_session, title="Midterm Review", owner_id=test_user.user_id, status=SessionStatus.ACTIVE
    )
    assert session.session_id
    assert session.title == "Midterm Review"
    assert session.status == SessionStatus.ACTIVE
    assert not session.deleted


def test_study_session_creation_no_title(db_session: Session, test_user: User):
    """Boundary test for study session creation with no title."""
    with pytest.raises(ValueError):
        StudySessionCtrl.create(db=db_session, title="", owner_id=test_user.user_id, status=SessionStatus.ACTIVE)


def test_study_session_creation_long_title(db_session: Session, test_user: User):
    """Boundary test for study session creation with a title that is too long."""
    long_title = "a" * (CALENDAR_TITLE[1] + 1)
    with pytest.raises(ValueError):
        StudySessionCtrl.create(db=db_session, title=long_title, owner_id=test_user.user_id, status=SessionStatus.ACTIVE)
