from sqlalchemy.orm import Session
import pytest

from src.classes import Poll
from src.controllers.polls import PollCtrl


def test_poll_creation(db_session: Session):
    """Black-box test for poll creation."""
    poll = PollCtrl.create(
        db=db_session,
        question="What is your favorite color?",
        options=["Red", "Green", "Blue"],
    )
    assert poll.poll_id
    assert poll.question == "What is your favorite color?"
    assert not poll.deleted


def test_poll_creation_no_question(db_session: Session):
    """Boundary test for poll creation with no question."""
    with pytest.raises(ValueError):
        PollCtrl.create(db=db_session, question="", options=["Yes", "No"])


def test_poll_creation_not_enough_options(db_session: Session):
    """Boundary test for poll creation with less than two options."""
    with pytest.raises(ValueError):
        PollCtrl.create(db=db_session, question="Is this a test?", options=["Yes"])


def test_poll_soft_delete(db_session: Session):
    """White-box test for poll soft delete."""
    poll = PollCtrl.create(
        db=db_session,
        question="Will this be deleted?",
        options=["Yes", "No"],
    )
    PollCtrl.safe_delete(poll, db_session)
    deleted_poll = PollCtrl.load(poll.poll_id, db_session)
    assert deleted_poll is None

    deleted_poll_in_db = db_session.query(Poll).filter(Poll.poll_id == poll.poll_id).first()
    assert deleted_poll_in_db
    assert deleted_poll_in_db.deleted
