from sqlalchemy.orm import Session
import pytest

from src.classes.poll import Poll
from src.controllers.polls import PollCtrl
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


def test_poll_creation(db_session: Session, test_user: User):
    """Black-box test for poll creation."""
    poll = PollCtrl.create(
        db=db_session,
        question="What is your favorite color?",
        owner_id=test_user.user_id,
        options=["Red", "Green", "Blue"],
    )
    assert poll.poll_id
    assert poll.question == "What is your favorite color?"
    assert not poll.deleted


def test_poll_creation_no_question(db_session: Session, test_user: User):
    """Boundary test for poll creation with no question."""
    with pytest.raises(ValueError):
        PollCtrl.create(
            db=db_session, question="", owner_id=test_user.user_id, options=["Yes", "No"]
        )


def test_poll_soft_delete(db_session: Session, test_user: User):
    """White-box test for poll soft delete."""
    poll = PollCtrl.create(
        db=db_session,
        question="Will this be deleted?",
        owner_id=test_user.user_id,
        options=["Yes", "No"],
    )
    PollCtrl.safe_delete(poll, db_session)
    deleted_poll = PollCtrl.load(poll.poll_id, db_session)
    assert deleted_poll is None

    deleted_poll_in_db = db_session.query(Poll).filter(Poll.poll_id == poll.poll_id).first()
    assert deleted_poll_in_db
    assert deleted_poll_in_db.deleted
