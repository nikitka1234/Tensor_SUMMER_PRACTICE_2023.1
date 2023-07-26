import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import auth_backend
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreate, UserUpdate

from fastapi import APIRouter, Depends

from src.api.deps import fastapi_users, current_user
from src.auth.service import crud_user
from src.database import get_async_session

from src.auth import schemas as user_schemas
from src.chat import schemas as chat_schemas
from src.search import schemas as search_schemas
from src.search.service import crud_tag, crud_user_tags

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

# users_router = {
#     "router": fastapi_users.get_users_router(UserRead, UserUpdate),
#     "prefix": "/users",
#     "tags": ["users"]
# }

users_router = APIRouter(prefix="/users", tags=["users"])
additional_users_router = APIRouter(prefix="/current", tags=["current"])


@users_router.get("/{id}", response_model=UserRead)
async def get_user_by_id(
        id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    user = (await session.scalars(select(User).filter(User.id == id))).all()
    return user


@additional_users_router.get("", response_model=UserRead)
async def get_user(user: User = Depends(current_user)):
    return user


@additional_users_router.get("/tags", response_model=list[search_schemas.Tag])
async def user_tags(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    tags_obj = (await session.scalars(user.tags.statement.offset(offset).limit(limit))).all()
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


@additional_users_router.put("", response_model=UserRead)
async def update_user(
        user_update: UserUpdate, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    user_obj = await crud_user.update(session, db_obj=user, obj_in=user_update)
    return user_obj


@additional_users_router.delete("", response_model=UserRead)
async def remove_user_by_id(
        user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    await session.delete(user)
    await session.commit()
    return user


router.include_router(**auth_router)
router.include_router(**register_router)
router.include_router(**verify_router)
router.include_router(**reset_password_router)
router.include_router(users_router)
router.include_router(additional_users_router)
