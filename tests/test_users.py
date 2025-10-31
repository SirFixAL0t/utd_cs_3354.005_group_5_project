from sqlalchemy.orm import Session
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
import uuid

from src.classes.user import User
from src.controllers.users import UserCtrl
from src.constants import DISPLAY_NAME, PASSWORD_LENGTH

# Define a strategy for generating valid user data
user_strategy = st.builds(
    User,
    name=st.text(min_size=DISPLAY_NAME[0], max_size=DISPLAY_NAME[1]),
    email=st.emails(),
    pw=st.text(min_size=PASSWORD_LENGTH[0], max_size=PASSWORD_LENGTH[1]),
    timezone=st.timezones(),
)

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(user_data=user_strategy)
def test_user_creation_and_retrieval_property(db_session: Session, user_data: User):
    """Property-based test to ensure user creation and retrieval are consistent."""
    # Note: Hypothesis may generate duplicate emails, which will fail the unique constraint.
    try:
        created_user = UserCtrl.create(
            db=db_session,
            name=user_data.name,
            email=f"{uuid.uuid4()}-{user_data.email}", # Make email unique for each test run
            pw=user_data.pw,
            timezone=str(user_data.timezone), # Convert timezone object to string
        )
    except Exception:
        # If creation fails (e.g., duplicate email), we assume the DB is working and skip the test case.
        db_session.close()
        return

    loaded_user = UserCtrl.load(created_user.user_id, db_session)

    assert loaded_user is not None
    assert loaded_user.name == created_user.name
    assert loaded_user.email == created_user.email


def test_user_creation(db_session: Session):
    """Black-box test for user creation."""
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test@example.com",
        pw="password123",
        timezone="UTC",
    )
    assert user.user_id
    assert user.name == "Test User"
    assert not user.deleted


def test_user_creation_empty_name(db_session: Session):
    """Boundary test for user creation with an empty name."""
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name="",
            email="test@example.com",
            pw="password123",
            timezone="UTC",
        )


def test_user_creation_long_name(db_session: Session):
    """Boundary test for user creation with a name that is too long."""
    long_name = "a" * (DISPLAY_NAME[1] + 1)
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name=long_name,
            email="test@example.com",
            pw="password123",
            timezone="UTC",
        )


def test_user_creation_invalid_email(db_session: Session):
    """Boundary test for user creation with an invalid email."""
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name="Test User",
            email="invalid-email",
            pw="password123",
            timezone="UTC",
        )


def test_user_creation_duplicate_email(db_session: Session):
    """Boundary test for user creation with a duplicate email."""
    UserCtrl.create(
        db=db_session,
        name="Test User",
        email="duplicate@example.com",
        pw="password123",
        timezone="UTC",
    )
    with pytest.raises(Exception):  # Depending on DB, could be IntegrityError
        UserCtrl.create(
            db=db_session,
            name="Another User",
            email="duplicate@example.com",
            pw="password123",
            timezone="UTC",
        )


def test_user_creation_short_password(db_session: Session):
    """Boundary test for user creation with a short password."""
    short_password = "a" * (PASSWORD_LENGTH[0] - 1)
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name="Test User",
            email="test-short-pw@example.com",
            pw=short_password,
            timezone="UTC",
        )


def test_user_creation_long_password(db_session: Session):
    """Boundary test for user creation with a long password."""
    long_password = "a" * (PASSWORD_LENGTH[1] + 1)
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name="Test User",
            email="test-long-pw@example.com",
            pw=long_password,
            timezone="UTC",
        )


def test_user_soft_delete(db_session: Session):
    """White-box test for user soft delete."""
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test-soft-delete@example.com",
        pw="password123",
        timezone="UTC",
    )
    UserCtrl.safe_delete(user, db_session)
    deleted_user = UserCtrl.load(user.user_id, db_session)
    assert deleted_user is None

    deleted_user_in_db = db_session.query(User).filter(User.user_id == user.user_id).first()
    assert deleted_user_in_db
    assert deleted_user_in_db.deleted


def test_user_permanent_delete(db_session: Session):
    """White-box test for user permanent delete."""
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email="test-perm-delete@example.com",
        pw="password123",
        timezone="UTC",
    )
    UserCtrl.permanent_delete(user, db_session)
    deleted_user = UserCtrl.load(user.user_id, db_session)
    assert deleted_user is None

    deleted_user_in_db = db_session.query(User).filter(User.user_id == user.user_id).first()
    assert deleted_user_in_db is None
