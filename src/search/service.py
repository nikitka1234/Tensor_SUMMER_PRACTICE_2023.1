import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud_base import CRUDBase
from src.search.models import Tag, UserTags, ChatTags, Category
from src.search.schemas import (
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
    async def exist_create(self, db: AsyncSession, *, tags: list[TagCreate]) -> list[Tag]:
        tags_title = [tag.title for tag in tags]
        q = select(self.model).where(self.model.title.in_(tags_title))
        result = await db.execute(q)
        curr = list(result.scalars())
        curr_titles = [c.title for c in curr]
        tags = [tag for tag in tags if tag.title not in curr_titles]

        for tag in tags:
            tag_obj = await self.create(db, obj_in=tag)
            curr.append(tag_obj)

        return curr


class CRUDUserTags(CRUDBase[UserTags, UserTagsCreate, UserTagsUpdate]):
    async def get_by_parameters(
            self, db: AsyncSession, *, user_id: uuid.UUID | int, tag_id: uuid.UUID | int
    ) -> UserTags:
        q = select(self.model).where(self.model.user_id == user_id, self.model.tag_id == tag_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDChatTags(CRUDBase[ChatTags, ChatTagsCreate, ChatTagsUpdate]):
    async def get_by_parameters(
            self, db: AsyncSession, *, chat_id: uuid.UUID | int, tag_id: uuid.UUID | int
    ) -> ChatTags:
        q = select(self.model).where(self.model.chat_id == chat_id, self.model.tag_id == tag_id)
        result = await db.execute(q)
        curr = result.scalar()
        return curr


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


crud_tag = CRUDTag(Tag)
crud_user_tags = CRUDUserTags(UserTags)
crud_chat_tags = CRUDChatTags(ChatTags)
crud_category = CRUDCategory(Category)
