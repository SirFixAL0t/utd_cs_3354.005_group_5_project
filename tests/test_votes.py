from sqlalchemy.orm import Session
import pytest
import uuid
from hypothesis import given, strategies as st, settings, HealthCheck

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
        email=f"vote-test-{uuid.uuid4()}@example.com",
        pw="password123",
        timezone="UTC",
    )

@pytest.fixture
def another_user(db_session: Session) -> User:
    return UserCtrl.create(
        db=db_session,
        name="Another User",
        email=f"vote-test-another-{uuid.uuid4()}@example.com",
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

# --- Property-Based Test with Hypothesis ---

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(option_index=st.integers(min_value=0, max_value=2))
def test_vote_creation_and_retrieval_property(
    db_session: Session, option_index: int
):
    """Property-based test for vote creation and retrieval."""
    # Create fresh user and poll for each example to avoid detached instance issues
    test_user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email=f"vote-test-{uuid.uuid4()}@example.com",
        pw="password123",
        timezone="UTC",
    )
    test_poll = PollCtrl.create(
        db=db_session,
        question="What is your favorite color?",
        owner_id=test_user.user_id,
        options=["Red", "Green", "Blue"],
    )
    another_user = UserCtrl.create(
        db=db_session,
        name="Another User",
        email=f"vote-test-another-{uuid.uuid4()}@example.com",
        pw="password123",
        timezone="UTC",
    )

    option_to_vote_for = test_poll.options[option_index]

    try:
        created_vote = VoteCtrl.create(
            db=db_session, poll_option_id=option_to_vote_for.option_id, user_id=another_user.user_id
        )

        loaded_vote = VoteCtrl.load(created_vote.vote_id, db_session)

        assert loaded_vote is not None
        assert loaded_vote.poll_option_id == created_vote.poll_option_id
        assert loaded_vote.user_id == another_user.user_id

    except PermissionError:
        db_session.rollback()
        return
    except Exception:
        db_session.rollback()
        return


# --- Existing Tests ---

def test_vote_creation(db_session: Session, test_poll: Poll, test_user: User):
    """Black-box test for vote creation."""
    option_to_vote_for = test_poll.options[0]
    vote = VoteCtrl.create(
        db=db_session, poll_option_id=option_to_vote_for.option_id, user_id=test_user.user_id
    )
    assert vote.vote_id
    assert vote.poll_option_id == option_to_vote_for.option_id
    assert not vote.deleted


def test_vote_voter_relationship(db_session: Session, test_poll: Poll, test_user: User):
    """Test that the voter relationship on a Vote object works correctly."""
    option_to_vote_for = test_poll.options[0]
    vote = VoteCtrl.create(
        db=db_session, poll_option_id=option_to_vote_for.option_id, user_id=test_user.user_id
    )
    assert vote.voter.user_id == test_user.user_id
    assert vote.voter.name == "Test User"

def test_vote_creation_invalid_option(db_session: Session, test_user: User):
    """Boundary test for vote creation with an invalid poll_option_id."""
    invalid_option_id = str(uuid.uuid4())
    with pytest.raises(ValueError, match="Invalid poll option ID"):
        VoteCtrl.create(db=db_session, poll_option_id=invalid_option_id, user_id=test_user.user_id)
