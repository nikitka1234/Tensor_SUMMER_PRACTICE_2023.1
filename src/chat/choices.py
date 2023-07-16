from enum import Enum


class ChatType(str, Enum):
    private: str = "private"
    group: str = "group"
    event: str = "event"


class UserRole(str, Enum):
    user: str = "user"
    admin: str = "admin"
    moderator: str = "moderator"
