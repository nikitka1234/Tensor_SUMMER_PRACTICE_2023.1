from enum import Enum


class ChatType(Enum):
    private: str = "private"
    group: str = "group"
    event: str = "event"


class UserRole(Enum):
    user: str = "user"
    admin: str = "admin"
    moderator: str = "moderator"
