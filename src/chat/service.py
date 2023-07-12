from src.api.crud_base import CRUDBase
from .models import Message, UserChats, Chat
from .schemas import (
    MessageCreate,
    MessageUpdate,
    UserChatsCreate,
    UserChatsUpdate,
    ChatCreate,
    ChatUpdate
)


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    pass


class CRUDUserChats(CRUDBase[UserChats, UserChatsCreate, UserChatsUpdate]):
    pass


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    pass


crud_message = CRUDMessage(Message)
crud_user_chats = CRUDUserChats(UserChats)
crud_chat = CRUDChat(Chat)
