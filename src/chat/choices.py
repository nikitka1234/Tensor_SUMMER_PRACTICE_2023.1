from enum import Enum


class ChatType(str, Enum):
    private: str = "private"
    group: str = "group"
    event: str = "event"
    channel: str = "channel"


class MessageType(str, Enum):
    text: str = "text"
    media: str = "media"
    audio: str = "audio"
    file: str = "file"
    text_media: str = "text_media"


class UserRole(str, Enum):
    user: str = "user"
    admin: str = "admin"
    moderator: str = "moderator"
