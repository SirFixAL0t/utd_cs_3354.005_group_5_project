from sqlalchemy.orm import Session
import pytest

from src.classes.friend import Friend
from src.classes.user import User
from src.controllers.friends import FriendsCtrl
from src.controllers.users import UserCtrl
from src.enums import FriendStatus
from src.constants import DISPLAY_NAME


@pytest.fixture
def test_users(db_session: Session) -> list[User]:
    user1 = UserCtrl.create(
        db=db_session,
        name="Test User 1",
        email="friend-test1@example.com",
        pw="password123",
        timezone="UTC",
    )
    user2 = UserCtrl.create(
        db=db_session,
        name="Test User 2",
        email="friend-test2@example.com",
        pw="password123",
        timezone="UTC",
    )
    return [user1, user2]


def test_friend_creation(db_session: Session, test_users: list[User]):
    """Black-box test for friend creation."""
    friendship = FriendsCtrl.create(
        db=db_session,
        left_id=test_users[0].user_id,
        right_id=test_users[1].user_id,
        status=FriendStatus.ACTIVE,
        nickname="Buddy",
    )
    assert friendship.friendship_id
    assert friendship.status == FriendStatus.ACTIVE
    assert not friendship.deleted


def test_friend_creation_self_friendship(db_session: Session, test_users: list[User]):
    """Boundary test for creating a friendship with oneself."""
    with pytest.raises(ValueError):
        FriendsCtrl.create(
            db=db_session,
            left_id=test_users[0].user_id,
            right_id=test_users[0].user_id,
            status=FriendStatus.ACTIVE,
            nickname="Me",
        )


def test_friend_creation_long_nickname(db_session: Session, test_users: list[User]):
    """Boundary test for creating a friendship with a nickname that is too long."""
    long_nickname = "a" * (DISPLAY_NAME[1] + 1)
    with pytest.raises(ValueError):
        FriendsCtrl.create(
            db=db_session,
            left_id=test_users[0].user_id,
            right_id=test_users[1].user_id,
            status=FriendStatus.ACTIVE,
            nickname=long_nickname,
        )


def test_friend_soft_delete(db_session: Session, test_users: list[User]):
    """White-box test for friend soft delete."""
    friendship = FriendsCtrl.create(
        db=db_session,
        left_id=test_users[0].user_id,
        right_id=test_users[1].user_id,
        status=FriendStatus.ACTIVE,
        nickname="Pal",
    )
    FriendsCtrl.safe_delete(friendship, db_session)
    deleted_friendship = FriendsCtrl.load(friendship.friendship_id, db_session)
    assert deleted_friendship is None

    deleted_friendship_in_db = (
        db_session.query(Friend).filter(Friend.friendship_id == friendship.friendship_id).first()
    )
    assert deleted_friendship_in_db
    assert deleted_friendship_in_db.deleted

def test_friend_user_relationships(db_session: Session, test_users: list[User]):
    """Test that the user relationships on a Friend object work correctly."""
    friendship = FriendsCtrl.create(
        db=db_session,
        left_id=test_users[0].user_id,
        right_id=test_users[1].user_id,
        status=FriendStatus.ACTIVE,
        nickname="Amigo",
    )
    assert friendship.left_user.name == "Test User 1"
    assert friendship.right_user.name == "Test User 2"
