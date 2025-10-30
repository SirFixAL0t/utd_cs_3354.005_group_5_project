from sqlalchemy.orm import Session
import pytest

from src.classes.poll import Poll
from src.controllers.polls import PollCtrl
from src.controllers.poll_options import PollOptionCtrl
from src.controllers.users import UserCtrl
from src.classes.user import User


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email="poll-option-test@example.com",
        pw="password123",
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
    long_text = "a" * 256
    with pytest.raises(ValueError):
        PollOptionCtrl.create(db=db_session, poll_id=test_poll.poll_id, option_text=long_text)
