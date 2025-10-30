from sqlalchemy import Column, String, Boolean, ForeignKey, event
from src.base_class import Base, default_uuid
from src.enums import FriendStatus


class Friend(Base):
    __tablename__ = 'friends'
    friendship_id = Column(String, primary_key=True, default=default_uuid)
    left_id = Column(String, ForeignKey('users.user_id'))
    right_id = Column(String, ForeignKey('users.user_id'))
    status = Column(String)
    nickname = Column(String)
    deleted = Column(Boolean, default=False, nullable=False)

    def set_status(self, status: FriendStatus) -> None:
        self.status = status

    @property
    def friendship_valid(self) -> bool:
        return self.status == FriendStatus.ACTIVE

    def accept_friendship(self) -> None:
        self.set_status(FriendStatus.ACTIVE)

    def remove_friend(self) -> None:
        self.set_status(FriendStatus.TERMINATED)

    def block_friend(self) -> None:
        self.set_status(FriendStatus.BLOCKED)

    def set_nickname(self, nick: str) -> None:
        self.nickname = nick



@event.listens_for(Friend, 'before_insert')
@event.listens_for(Friend, 'before_update')
def validate_friend(mapper, connection, target):
    from src.validators.friend import FriendValidator
    FriendValidator().validate(target)
