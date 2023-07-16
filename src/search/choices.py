from enum import Enum


class Holder(str, Enum):
    user: str = "user"
    chat: str = "chat"
