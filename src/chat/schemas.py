import uuid

from pydantic import BaseModel
from datetime import datetime

from src.chat.choices import ChatType, UserRole


###################
# Message schemas #
###################

class MessageBase(BaseModel):
    text: str
    external: dict | None = None


class MessageCreate(MessageBase):
    user_id: uuid.UUID
    chat_id: uuid.UUID


class MessageUpdate(MessageBase):
    updated_at: datetime
    deleted_at: datetime | None = None


#####################
# UserChats schemas #
#####################

class UserChatsBase(BaseModel):
    role: UserRole | str = UserRole.user


class UserChatsCreate(UserChatsBase):
    user_id: uuid.UUID
    chat_id: uuid.UUID


class UserChatsUpdate(UserChatsBase):
    updated_at: datetime
    deleted_at: datetime | None = None


################
# Chat schemas #
################

class ChatBase(BaseModel):
    type: ChatType | str
    external: dict | None = None
    parent_id: uuid.UUID | None = None


class ChatCreate(ChatBase):
    pass


class ChatUpdate(ChatBase):
    updated_at: datetime
    deleted_at: datetime | None = None
