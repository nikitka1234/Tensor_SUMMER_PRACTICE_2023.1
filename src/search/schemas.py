import uuid

from pydantic import BaseModel
from datetime import datetime

from src.chat.choices import ChatType, UserRole


###############
# Tag schemas #
###############

class TagBase(BaseModel):
    category_id: uuid.UUID
    title: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    deleted_at: datetime | None = None


class TagInDB(TagBase):
    id: uuid.UUID
    created_at: datetime
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True


class Tag(TagInDB):
    pass



####################
# UserTags schemas #
####################

class UserTagsBase(BaseModel):
    user_id: uuid.UUID
    tag_id: uuid.UUID


class UserTagsCreate(UserTagsBase):
    pass


class UserTagsUpdate(UserTagsBase):
    deleted_at: datetime | None = None


class UserTagsInDB(UserTagsBase):
    id: uuid.UUID
    created_at: datetime
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True


class UserTags(UserTagsInDB):
    pass


####################
# ChatTags schemas #
####################

class ChatTagsBase(BaseModel):
    chat_id: uuid.UUID
    tag_id: uuid.UUID


class ChatTagsCreate(ChatTagsBase):
    pass


class ChatTagsUpdate(ChatTagsBase):
    deleted_at: datetime | None = None


class ChatTagsInDB(ChatTagsBase):
    id: uuid.UUID
    created_at: datetime
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True


class ChatTags(ChatTagsInDB):
    pass


####################
# Category schemas #
####################

class CategoryBase(BaseModel):
    title: str
    external: dict | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    updated_at: datetime
    deleted_at: datetime | None = None


class CategoryInDB(CategoryBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None

    class Config:
        orm_mode = True


class Category(CategoryInDB):
    pass
