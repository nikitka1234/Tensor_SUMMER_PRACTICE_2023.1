import uuid

from pydantic import BaseModel

from src.chat.choices import ChatType, UserRole

from src.search.schemas import Tag


###################
# Message schemas #
###################

class MessageBase(BaseModel):
    text: str
    external: dict | None = None


class MessageCreate(MessageBase):
    chat_id: uuid.UUID


class MessageUpdate(MessageBase):
    pass


class MessageDB(BaseModel):
    id: uuid.UUID
    text: str
    user_id: uuid.UUID
    chat_id: uuid.UUID
    external: dict

    class Config:
        orm_mode = True


class Message(MessageDB):
    pass


#####################
# UserChats schemas #
#####################

class UserChatsBase(BaseModel):
    role: UserRole = UserRole.user


class UserChatsCreate(UserChatsBase):
    user_id: uuid.UUID
    chat_id: uuid.UUID


class UserChatsUpdate(UserChatsBase):
    pass


class UserChatsDB(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    chat_id: uuid.UUID
    role: UserRole

    class Config:
        orm_mode = True


class UserChats(UserChatsDB):
    pass


################
# Chat schemas #
################

class ChatBase(BaseModel):
    external: dict | None = None
    parent_id: uuid.UUID | None = None


class ChatCreate(ChatBase):
    type: ChatType = ChatType.private


class ChatUpdate(ChatBase):
    pass


class ChatDB(BaseModel):
    id: uuid.UUID
    type: ChatType
    external: dict
    parent_id: uuid.UUID | None

    # tags: list[Tag]

    class Config:
        orm_mode = True


class Chat(ChatDB):
    pass
