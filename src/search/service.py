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
    pass


class CRUDChatTags(CRUDBase[ChatTags, ChatTagsCreate, ChatTagsUpdate]):
    pass


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


crud_tag = CRUDTag(Tag)
crud_user_tags = CRUDUserTags(UserTags)
crud_chat_tags = CRUDChatTags(ChatTags)
crud_category = CRUDCategory(Category)
