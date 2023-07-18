import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud_base import CRUDBase
from .models import Tag, UserTags, ChatTags, Category
from .schemas import (
    TagCreate,
    TagUpdate,
    UserTagsCreate,
    UserTagsUpdate,
    ChatTagsCreate,
    ChatTagsUpdate,
    CategoryCreate,
    CategoryUpdate
)


class CRUDTag(CRUDBase[Tag, TagCreate, TagUpdate]):
    pass


class CRUDUserTags(CRUDBase[UserTags, UserTagsCreate, UserTagsUpdate]):
    async def get_by_parameters(
            self, db: AsyncSession, *, user_id: uuid.UUID | int, tag_id: uuid.UUID | int
    ) -> UserTags:
        q = select(self.model).where(self.model.user_id == user_id and self.model.tag_id == tag_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDChatTags(CRUDBase[ChatTags, ChatTagsCreate, ChatTagsUpdate]):
    async def get_by_parameters(
            self, db: AsyncSession, *, chat_id: uuid.UUID | int, tag_id: uuid.UUID | int
    ) -> ChatTags:
        q = select(self.model).where(self.model.chat_id == chat_id and self.model.tag_id == tag_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


crud_tag = CRUDTag(Tag)
crud_user_tags = CRUDUserTags(UserTags)
crud_chat_tags = CRUDChatTags(ChatTags)
crud_category = CRUDCategory(Category)
