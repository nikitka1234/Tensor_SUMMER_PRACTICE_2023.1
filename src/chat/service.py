import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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
    async def create_user(
            self,
            db: AsyncSession,
            *,
            user_id: uuid.UUID,
            obj_in: MessageCreate
    ) -> Message:
        obj_in_data = jsonable_encoder(obj_in)
        obj_in_data["user_id"] = user_id
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


class CRUDUserChats(CRUDBase[UserChats, UserChatsCreate, UserChatsUpdate]):
    async def get_by_parameters(
            self, db: AsyncSession, *, chat_id: uuid.UUID | int, user_id: uuid.UUID | int
    ) -> UserChats:
        q = select(self.model).where(self.model.chat_id == chat_id and self.model.user_id == user_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    pass


crud_message = CRUDMessage(Message)
crud_user_chats = CRUDUserChats(UserChats)
crud_chat = CRUDChat(Chat)
