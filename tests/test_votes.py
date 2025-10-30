from sqlalchemy.orm import Session
import pytest

from src.classes.poll import Poll
from src.controllers.polls import PollCtrl
from src.controllers.votes import VoteCtrl
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

@pytest.fixture
def test_poll(db_session: Session, test_user: User) -> Poll:
    return PollCtrl.create(
        db=db_session,
        question="What is your favorite color?",
        owner_id=test_user.user_id,
        options=["Red", "Green", "Blue"],
    )


def test_vote_creation(db_session: Session, test_poll: Poll, test_user: User):
    """Black-box test for vote creation."""
    option_to_vote_for = test_poll.options[0]
    vote = VoteCtrl.create(
        db=db_session, poll_option_id=option_to_vote_for.option_id, user_id=test_user.user_id
    )
    assert vote.vote_id
    assert vote.poll_option_id == option_to_vote_for.option_id
    assert not vote.deleted
