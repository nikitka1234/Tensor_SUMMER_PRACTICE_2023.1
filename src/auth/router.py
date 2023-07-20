import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from .auth import auth_backend
from .models import User
from .schemas import UserRead, UserCreate, UserUpdate

from fastapi import APIRouter, Depends

from src.api.deps import fastapi_users, current_user
from ..database import get_async_session

from ..auth import schemas as user_schemas
from ..chat import schemas as chat_schemas
from ..search import schemas as search_schemas
from ..search.service import crud_tag, crud_user_tags

router = APIRouter()

auth_router = {
    "router": fastapi_users.get_auth_router(auth_backend),
    "prefix": "/auth/jwt",
    "tags": ["auth"]
}

register_router = {
    "router": fastapi_users.get_register_router(UserRead, UserCreate),
    "prefix": "/auth",
    "tags": ["auth"]
}

verify_router = {
    "router": fastapi_users.get_verify_router(UserRead),
    "prefix": "/auth",
    "tags": ["auth"]
}

reset_password_router = {
    "router": fastapi_users.get_reset_password_router(),
    "prefix": "/auth",
    "tags": ["auth"]
}

users_router = {
    "router": fastapi_users.get_users_router(UserRead, UserUpdate),
    "prefix": "/users",
    "tags": ["users"]
}

additional_users_router = APIRouter(prefix="/users", tags=["users"])


@additional_users_router.get("/tags", response_model=list[search_schemas.Tag])
async def user_tags(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = (await session.scalars(user.tags.statement)).all()[offset:offset+limit]
    return tags_obj


@additional_users_router.post("/tags", response_model=list[search_schemas.Tag])
async def update_user_tags(
        tags: list[search_schemas.TagCreate],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = await crud_tag.exist_create(session, tags=tags)

    for tag in tags_obj:
        user_tags_create = search_schemas.UserTagsCreate(user_id=user.id, tag_id=tag.id)
        await crud_user_tags.create(session, obj_in=user_tags_create)

    return tags_obj


# @additional_users_router.put("/tags", response_model=list[search_schemas.Tag])
# async def create_user_tags(
#         tags_id: list[uuid.UUID],
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     tags_obj = []
#
#     for tag_id in tags_id:
#         tag_obj = await crud_tag.get(session, model_id=tag_id)
#         user_tags_create = search_schemas.UserTagsCreate(user_id=user.id, tag_id=tag_obj.id)
#         await crud_user_tags.create(session, obj_in=user_tags_create)
#         tags_obj.append(tag_obj)
#
#     return tags_obj
#
#
# @additional_users_router.delete("/tags", response_model=list[search_schemas.Tag])
# async def create_user_tags(
#         tags_id: list[uuid.UUID],
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     tags_obj = []
#
#     for tag_id in tags_id:
#         tag_obj = await crud_tag.get(session, model_id=tag_id)
#         user_tags_create = search_schemas.UserTagsCreate(user_id=user.id, tag_id=tag_obj.id)
#         await crud_user_tags.create(session, obj_in=user_tags_create)
#         tags_obj.append(tag_obj)
#
#     return tags_obj


router.include_router(**auth_router)
router.include_router(**register_router)
router.include_router(**verify_router)
router.include_router(**reset_password_router)
router.include_router(**users_router)
router.include_router(additional_users_router)
