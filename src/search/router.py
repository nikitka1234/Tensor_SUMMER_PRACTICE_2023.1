import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.search.service import crud_tag, crud_user_tags, crud_chat_tags, crud_category

from src.search.choices import Holder
from src.api.deps import current_user, current_superuser

from src.auth.models import User
from src.auth import schemas as user_schemas
from src.chat import schemas as chat_schemas
from src.search import schemas as search_schemas

category_router = APIRouter(prefix="/categories", tags=["categories"])
tag_router = APIRouter(prefix="/tags", tags=["tags"])


######################
# Category endpoints #
######################


@category_router.get("", response_model=list[search_schemas.Category])
async def categories(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    categories_obj = await crud_category.get_multi(session, offset=offset, limit=limit)
    return categories_obj


@category_router.get("/{category_id}", response_model=search_schemas.Category)
async def category(
        category_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    category_obj = await crud_category.get(session, model_id=category_id)
    return category_obj


# @category_router.get("/{category_id}/tags", response_model=list[search_schemas.Tag])
# async def category_tags(
#         category_id: uuid.UUID,
#         offset: 0,
#         limit: 100,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     category_obj = await crud_category.get(session, model_id=category_id)
#     tags_obj = (await session.scalars(category_obj.tags.statement.offset(offset).limit(limit))).all()
#     return tags_obj


@category_router.post("", response_model=list[search_schemas.Category])
async def create_category(
        categories: list[search_schemas.CategoryCreate],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    categories_obj = []

    for category in categories:
        category_obj = await crud_category.create(session, obj_in=category)
        categories_obj.append(category_obj)

    return categories_obj


@category_router.put("", response_model=search_schemas.Category)
async def update_category(
        category_id: uuid.UUID,
        category: search_schemas.CategoryUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    category_obj = await crud_category.get(session, model_id=category_id)
    updated_category_obj = await crud_category.update(session, db_obj=category_obj, obj_in=category)
    return updated_category_obj


@category_router.delete("", response_model=list[search_schemas.Category])
async def delete_category(
        categories_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    deleted_categories_obj = []

    for category_id in categories_id:
        deleted_category_obj = await crud_category.delete(session, model_id=category_id)
        deleted_categories_obj.append(deleted_category_obj)

    return deleted_categories_obj


#################
# Tag endpoints #
#################


@tag_router.get("", response_model=list[search_schemas.Tag])
async def tags(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = await crud_tag.get_multi(session, offset=offset, limit=limit)
    return tags_obj


@tag_router.get("/{tag_id}", response_model=search_schemas.Tag)
async def tag(
        tag_id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.get(session, model_id=tag_id)
    return tag_obj


@tag_router.get("/{tag_id}/category", response_model=search_schemas.Category)
async def tag_category(
        tag_id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.get(session, model_id=tag_id)
    return tag_obj.category


@tag_router.get("/{tag_id}/users", response_model=list[user_schemas.UserRead])
async def tag_users(
        tag_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.get(session, model_id=tag_id)
    users_obj = (await session.scalars(tag_obj.users.statement.offset(offset).limit(limit))).all()
    return users_obj


@tag_router.get("/{tag_id}/chats", response_model=list[chat_schemas.Chat])
async def tag_chats(
        tag_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.get(session, model_id=tag_id)
    chats_obj = (await session.scalars(tag_obj.chats.statement.offset(offset).limit(limit))).all()
    return chats_obj


@tag_router.post("", response_model=search_schemas.Tag)
async def create_tag(
        tag: search_schemas.TagCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.create(session, obj_in=tag)
    return tag_obj


@tag_router.put("", response_model=search_schemas.Tag)
async def update_tag(
        tag_id: uuid.UUID,
        tag: search_schemas.TagUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tag_obj = await crud_tag.get(session, model_id=tag_id)
    updated_tag_obj = await crud_tag.update(session, db_obj=tag_obj, obj_in=tag)
    return updated_tag_obj


@tag_router.delete("", response_model=list[search_schemas.Tag])
async def delete_tag(
        tags_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    deleted_tags_obj = []

    for tag_id in tags_id:
        deleted_tag_obj = await crud_tag.delete(session, model_id=tag_id)
        deleted_tags_obj.append(deleted_tag_obj)

    return deleted_tags_obj
