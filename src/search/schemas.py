import uuid

from pydantic import BaseModel, Field
from datetime import datetime


###############
# Tag schemas #
###############

class TagBase(BaseModel):
    category_id: uuid.UUID
    title: str


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagDB(BaseModel):
    id: uuid.UUID
    category_id: uuid.UUID
    title: str = Field(max_length=320)

    created_at: datetime
    deleted_at: datetime | None

    class Config:
        orm_mode = True


class Tag(TagDB):
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
    pass


class UserTagsDB(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    tag_id: uuid.UUID

    created_at: datetime
    deleted_at: datetime | None

    class Config:
        orm_mode = True


class UserTags(UserTagsDB):
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
    pass


class ChatTagsDB(BaseModel):
    id: uuid.UUID
    chat_id: uuid.UUID
    tag_id: uuid.UUID

    created_at: datetime
    deleted_at: datetime | None

    class Config:
        orm_mode = True


class ChatTags(ChatTagsDB):
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
    pass


class CategoryDB(BaseModel):
    id: uuid.UUID
    title: str = Field(max_length=320)
    external: dict

    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None

    # tags: list[Tag]

    class Config:
        orm_mode = True


class Category(CategoryDB):
    pass
