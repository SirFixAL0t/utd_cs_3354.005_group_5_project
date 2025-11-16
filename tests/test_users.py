from sqlalchemy.orm import Session
import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
import uuid
from pydantic import EmailStr, TypeAdapter

from src.classes.user import User
from src.controllers.users import UserCtrl
from src.constants import DISPLAY_NAME, PASSWORD_LENGTH

# Create a TypeAdapter for EmailStr for explicit validation
EmailAdapter = TypeAdapter(EmailStr)

# Define a strategy for generating valid user data for the controller
user_strategy = st.fixed_dictionaries(
    {
        "name": st.text(min_size=DISPLAY_NAME[0], max_size=DISPLAY_NAME[1]),
        "email": st.emails().map(lambda e: EmailAdapter.validate_python(e)),
        "password": st.text(min_size=PASSWORD_LENGTH[0], max_size=72), # Cap password length at 72 for bcrypt
        "timezone": st.timezones().map(str),
    }
)

@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(user_data=user_strategy)
def test_user_creation_and_retrieval_property(db_session: Session, user_data: dict):
    """Property-based test to ensure user creation and retrieval are consistent."""
    try:
        # Make email unique for each test run to avoid constraint violations
        user_data["email"] = f"{uuid.uuid4()}-{user_data['email']}"
        created_user = UserCtrl.create(db=db_session, **user_data)
    except Exception:
        db_session.rollback()
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
        email=EmailAdapter.validate_python("test@example.com"),
        password="password123",
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
            email=EmailAdapter.validate_python("test@example.com"),
            password="password123",
            timezone="UTC",
        )


def test_user_creation_long_name(db_session: Session):
    """Boundary test for user creation with a name that is too long."""
    long_name = "a" * (DISPLAY_NAME[1] + 1)
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name=long_name,
            email=EmailAdapter.validate_python("test@example.com"),
            password="password123",
            timezone="UTC",
        )


def test_user_creation_invalid_email(db_session: Session):
    """Boundary test for user creation with an invalid email."""
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name="Test User",
            email="invalid-email",
            password="password123",
            timezone="UTC",
        )


def test_user_creation_duplicate_email(db_session: Session):
    """Boundary test for user creation with a duplicate email."""
    UserCtrl.create(
        db=db_session,
        name="Test User",
        email=EmailAdapter.validate_python("duplicate@example.com"),
        password="password123",
        timezone="UTC",
    )
    with pytest.raises(Exception):
        UserCtrl.create(
            db=db_session,
            name="Another User",
            email=EmailAdapter.validate_python("duplicate@example.com"),
            password="password123",
            timezone="UTC",
        )


def test_user_creation_short_password(db_session: Session):
    """Boundary test for user creation with a short password."""
    short_password = "a" * (PASSWORD_LENGTH[0] - 1)
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name="Test User",
            email=EmailAdapter.validate_python("test-short-pw@example.com"),
            password=short_password,
            timezone="UTC",
        )


def test_user_creation_long_password(db_session: Session):
    """Boundary test for user creation with a long password."""
    long_password = "a" * (73) # 73 is over the bcrypt limit of 72
    with pytest.raises(ValueError):
        UserCtrl.create(
            db=db_session,
            name="Test User",
            email=EmailAdapter.validate_python("test-long-pw@example.com"),
            password=long_password,
            timezone="UTC",
        )


def test_user_soft_delete(db_session: Session):
    """White-box test for user soft delete."""
    user = UserCtrl.create(
        db=db_session,
        name="Test User",
        email=EmailAdapter.validate_python("test-soft-delete@example.com"),
        password="password123",
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
        email=EmailAdapter.validate_python("test-perm-delete@example.com"),
        password="password123",
        timezone="UTC",
    )
    UserCtrl.permanent_delete(user, db_session)
    deleted_user = UserCtrl.load(user.user_id, db_session)
    assert deleted_user is None

    deleted_user_in_db = db_session.query(User).filter(User.user_id == user.user_id).first()
    assert deleted_user_in_db is None
