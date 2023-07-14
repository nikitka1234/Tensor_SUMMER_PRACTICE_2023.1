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
