from sqlalchemy.orm import Session
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
import uuid
from pydantic import EmailStr, TypeAdapter

from src.classes.poll import Poll
from src.constants import POLL_QUESTION_LENGTH
from src.controllers.polls import PollCtrl
from src.controllers.votes import VoteCtrl
from src.controllers.users import UserCtrl
from src.classes.user import User

EmailAdapter = TypeAdapter(EmailStr)


@pytest.fixture
def test_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Test User",
        email=EmailAdapter.validate_python(f"poll-test-{uuid.uuid4()}@example.com"),
        password="password123",
        timezone="UTC",
    )

@pytest.fixture
def another_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Another User",
        email=EmailAdapter.validate_python(f"poll-test-another-{uuid.uuid4()}@example.com"),
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


poll_strategy = st.builds(
    Poll,
    question=st.text(min_size=POLL_QUESTION_LENGTH[0], max_size=POLL_QUESTION_LENGTH[1]),
    allow_multi_votes=st.booleans(),
)

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(poll_data=poll_strategy, options=st.lists(st.text(min_size=1, max_size=100), min_size=2, max_size=10))
def test_poll_creation_and_retrieval_property(
    db_session: Session, test_user: User, poll_data: Poll, options: list[str]
):
    """Property-based test for poll creation and retrieval."""
    try:
        created_poll = PollCtrl.create(
            db=db_session,
            question=poll_data.question,
            owner_id=test_user.user_id,
            options=options,
            allow_multi_votes=poll_data.allow_multi_votes,
        )
    except Exception:
        db_session.rollback()
        return

    loaded_poll = PollCtrl.load(created_poll.poll_id, db_session)

    assert loaded_poll is not None
    assert loaded_poll.question == created_poll.question
    assert len(loaded_poll.options) == len(options)


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

def test_get_votes(db_session: Session, test_poll: Poll, test_user: User, another_user: User):
    """Test retrieving all votes for a poll."""
    VoteCtrl.create(db_session, test_poll.options[0].option_id, test_user.user_id)
    VoteCtrl.create(db_session, test_poll.options[1].option_id, another_user.user_id)
    votes = PollCtrl.get_votes(test_poll, db_session)
    assert len(votes) == 2

def test_get_most_voted_option(db_session: Session, test_poll: Poll, test_user: User, another_user: User):
    """Test finding the most voted option in a poll."""
    VoteCtrl.create(db_session, test_poll.options[0].option_id, test_user.user_id)
    VoteCtrl.create(db_session, test_poll.options[0].option_id, another_user.user_id)
    most_voted = PollCtrl.get_most_voted_option(test_poll, db_session)
    assert most_voted.option_text == "Red"

def test_user_cannot_vote_on_closed_poll(db_session: Session, test_poll: Poll, test_user: User):
    """Test that a user cannot vote on a poll that has been closed."""
    PollCtrl.close_poll(test_poll, db_session)
    with pytest.raises(PermissionError, match="User is not allowed to vote on this poll."):
        VoteCtrl.create(db_session, test_poll.options[0].option_id, test_user.user_id)


def test_user_cannot_vote_twice(db_session: Session, test_poll: Poll, test_user: User):
    """Test that a user cannot vote more than once on a single-vote poll."""
    VoteCtrl.create(db_session, test_poll.options[0].option_id, test_user.user_id)
    with pytest.raises(PermissionError, match="User is not allowed to vote on this poll."):
        VoteCtrl.create(db_session, test_poll.options[1].option_id, test_user.user_id)

def test_user_can_vote_multiple_times_if_allowed(db_session: Session, test_user: User):
    """Test that a user can vote multiple times on a poll that allows it."""
    multi_vote_poll = PollCtrl.create(
        db=db_session,
        question="Pick multiple:",
        owner_id=test_user.user_id,
        options=["A", "B", "C"],
        allow_multi_votes=True,
    )
    VoteCtrl.create(db_session, multi_vote_poll.options[0].option_id, test_user.user_id)
    VoteCtrl.create(db_session, multi_vote_poll.options[1].option_id, test_user.user_id)
    votes = PollCtrl.get_votes(multi_vote_poll, db_session)
    assert len(votes) == 2
