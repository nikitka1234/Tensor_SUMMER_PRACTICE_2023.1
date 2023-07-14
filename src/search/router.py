import uuid

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .schemas import TagCreate, UserTagsCreate, ChatTagsCreate, CategoryCreate
from .service import crud_tag, crud_user_tags, crud_chat_tags, crud_category

from .choices import Holder

router = APIRouter()


@router.post("/new_category")
async def new_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    await crud_category.create(session, obj_in=category)


@router.post("/new_tag")
async def new_tag(tag: TagCreate, holder: Holder, holder_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    tag_obj = await crud_tag.create(session, obj_in=tag)

    if holder == Holder.user:
        user_tags_create = UserTagsCreate(user_id=holder_id, tag_id=tag_obj.id)
        await crud_user_tags.create(session, obj_in=user_tags_create)
    elif holder == Holder.chat:
        chat_tags_create = ChatTagsCreate(chat_id=holder_id, tag_id=tag_obj.id)
        await crud_chat_tags.create(session, obj_in=chat_tags_create)


# @router.post("")
