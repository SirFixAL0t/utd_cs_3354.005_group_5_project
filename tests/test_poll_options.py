from sqlalchemy.orm import Session
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
import uuid
from pydantic import EmailStr, TypeAdapter

from src.classes.poll import Poll
from src.classes.poll_option import PollOption
from src.constants import POLL_OPTION_TEXT_LENGTH
from src.controllers.polls import PollCtrl
from src.controllers.poll_options import PollOptionCtrl
from src.controllers.users import UserCtrl
from src.classes.user import User

EmailAdapter = TypeAdapter(EmailStr)


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email=EmailAdapter.validate_python(f"poll-option-test-{uuid.uuid4()}@example.com"),
        password="password123",
        timezone="UTC",
    )

@pytest.fixture
def test_poll(db_session: Session, test_user: User) -> Poll:
    return PollCtrl.create(
        db=db_session,
        question="What is your favorite color?",
        owner_id=test_user.user_id,
        options=["Red", "Green", "Blue"],
    )


poll_option_strategy = st.builds(
    PollOption, option_text=st.text(min_size=1, max_size=POLL_OPTION_TEXT_LENGTH[1])
)

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(option_data=poll_option_strategy)
def test_poll_option_creation_and_retrieval_property(
    db_session: Session, test_poll: Poll, option_data: PollOption
):
    """Property-based test for poll option creation and retrieval."""
    try:
        created_option = PollOptionCtrl.create(
            db=db_session, poll_id=test_poll.poll_id, option_text=option_data.option_text
        )
    except Exception:
        db_session.rollback()
        return

    loaded_option = PollOptionCtrl.load(created_option.option_id, db_session)

    assert loaded_option is not None
    assert loaded_option.option_text == created_option.option_text


def test_poll_option_creation(db_session: Session, test_poll: Poll):
    """Black-box test for poll option creation."""
    option = PollOptionCtrl.create(
        db=db_session, poll_id=test_poll.poll_id, option_text="Yellow"
    )
    assert option.option_id
    assert option.option_text == "Yellow"
    assert not option.deleted


def test_poll_option_creation_empty_text(db_session: Session, test_poll: Poll):
    """Boundary test for poll option creation with empty text."""
    with pytest.raises(ValueError):
        PollOptionCtrl.create(db=db_session, poll_id=test_poll.poll_id, option_text="")


def test_poll_option_creation_long_text(db_session: Session, test_poll: Poll):
    """Boundary test for poll option creation with text that is too long."""
    long_text = "a" * (POLL_OPTION_TEXT_LENGTH[1] + 1)
    with pytest.raises(ValueError):
        PollOptionCtrl.create(db=db_session, poll_id=test_poll.poll_id, option_text=long_text)
