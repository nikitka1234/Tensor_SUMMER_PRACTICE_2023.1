import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .schemas import TagCreate, UserTagsCreate, ChatTagsCreate, CategoryCreate
from .service import crud_tag, crud_user_tags, crud_chat_tags, crud_category

from .choices import Holder
from ..api.deps import current_user

from ..auth.models import User
from ..auth import schemas as user_schemas
from ..chat import schemas as chat_schemas
from ..search import schemas as search_schemas

router = APIRouter()


@router.post("/new_category", response_model=search_schemas.Category)
async def new_category(category: CategoryCreate, session: AsyncSession = Depends(get_async_session)):
    category_obj = await crud_category.create(session, obj_in=category)

    return category_obj


@router.post("/delete_category", response_model=search_schemas.Category)
async def new_category(category_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    category_obj = await crud_category.delete(session, model_id=category_id)

    return category_obj


@router.get("/categories", response_model=list[search_schemas.Category])
async def categories(session: AsyncSession = Depends(get_async_session)):
    return await crud_category.get_multi(session)


@router.post("/new_tag", response_model=search_schemas.Tag)
async def new_tag(
        tag: TagCreate, holder: Holder, holder_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.create(session, obj_in=tag)

    if holder == Holder.user:
        user_tags_create = UserTagsCreate(user_id=holder_id, tag_id=tag_obj.id)
        await crud_user_tags.create(session, obj_in=user_tags_create)
    elif holder == Holder.chat:
        chat_tags_create = ChatTagsCreate(chat_id=holder_id, tag_id=tag_obj.id)
        await crud_chat_tags.create(session, obj_in=chat_tags_create)

    return tag_obj


@router.post("/new_user_tag", response_model=search_schemas.Tag)
async def new_user_tag(
        tag: TagCreate, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.create(session, obj_in=tag)

    user_tags_create = UserTagsCreate(user_id=user.id, tag_id=tag_obj.id)
    await crud_user_tags.create(session, obj_in=user_tags_create)

    return tag_obj


@router.post("/new_chat_tag", response_model=search_schemas.Tag)
async def new_chat_tag(
        tag: TagCreate, chat_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.create(session, obj_in=tag)

    chat_tags_create = ChatTagsCreate(chat_id=chat_id, tag_id=tag_obj.id)
    await crud_chat_tags.create(session, obj_in=chat_tags_create)

    return tag_obj


@router.post("/delete_tag", response_model=search_schemas.Tag)
async def new_tag(
        tag_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.delete(session, model_id=tag_id)

    return tag_obj
