import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session

from src.chat.service import crud_chat, crud_message, crud_user_chats
from src.auth.models import User
from src.api.deps import current_user

from src.auth import schemas as user_schemas
from src.chat import schemas as chat_schemas
from src.search import schemas as search_schemas
from src.search.service import crud_chat_tags, crud_tag


chat_router = APIRouter(prefix="/chats", tags=["chats"])
message_router = APIRouter(prefix="/messages", tags=["messages"])


##################
# Chat endpoints #
##################


@chat_router.get("", response_model=list[chat_schemas.Chat])
async def user_chats(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chats_obj = (await session.scalars(user.chats.statement.offset(offset).limit(limit))).all()
    return chats_obj


@chat_router.get("/{chat_id}", response_model=chat_schemas.Chat)
async def chat(
        chat_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    return chat_obj


@chat_router.get("/{chat_id}/messages", response_model=list[chat_schemas.Message])
async def chat_messages(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    messages_obj = (await session.scalars(chat_obj.messages.statement.offset(offset).limit(limit))).all()
    return messages_obj


@chat_router.get("/{chat_id}/users", response_model=list[user_schemas.UserRead])
async def chat_users(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    users_obj = (await session.scalars(chat_obj.users.statement.offset(offset).limit(limit))).all()
    return users_obj


@chat_router.get("/{chat_id}/tags", response_model=list[chat_schemas.Tag])
async def chat_tags(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    tags_obj = (await session.scalars(chat_obj.tags.statement.offset(offset).limit(limit))).all()
    return tags_obj


@chat_router.post("", response_model=chat_schemas.Chat)
async def create_chat(
        chat: chat_schemas.ChatCreate,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.create(session, obj_in=chat)

    for user_id in users_id:
        user_chats_obj = chat_schemas.UserChatsCreate(user_id=user_id, chat_id=chat_obj.id)
        await crud_user_chats.create(session, obj_in=user_chats_obj)

    return chat_obj


@chat_router.post("/{chat_id}/tags", response_model=list[search_schemas.Tag])
async def update_chat_tags(
        tags: list[search_schemas.TagCreate],
        chat_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    tags_obj = await crud_tag.exist_create(session, tags=tags)

    for tag in tags_obj:
        chat_tags_create = search_schemas.ChatTagsCreate(user_id=chat_obj.id, tag_id=tag.id)
        await crud_chat_tags.create(session, obj_in=chat_tags_create)

    return tags_obj


@chat_router.put("/{chat_id}", response_model=chat_schemas.Chat)
async def update_chat(
        chat_id: uuid.UUID,
        chat: chat_schemas.ChatUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    updated_chat_obj = await crud_chat.update(session, db_obj=chat_obj, obj_in=chat)
    return updated_chat_obj


@chat_router.put("/{chat_id}/users")
async def add_chat_users(
        chat_id: uuid.UUID,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    for user_id in users_id:
        user_chats_obj = chat_schemas.UserChatsCreate(user_id=user_id, chat_id=chat_id)
        await crud_user_chats.create(session, obj_in=user_chats_obj)


@chat_router.delete("/{chat_id}", response_model=chat_schemas.Chat)
async def delete_chat(
        chat_id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    deleted_chat_obj = await crud_chat.delete(session, model_id=chat_id)
    return deleted_chat_obj


@chat_router.delete("/{chat_id}/users")
async def delete_chat_users(
        chat_id: uuid.UUID,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    for user_id in users_id:
        user_chats_obj = await crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user_id)
        deleted_user_chats_obj = await crud_user_chats.delete(session, model_id=user_chats_obj.id)


#####################
# Message endpoints #
#####################


@message_router.get("", response_model=list[chat_schemas.Message])
async def user_messages(
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    messages_obj = (await session.scalars(user.messages.statement.offset(offset).limit(limit))).all()
    return messages_obj


@message_router.get("/{message_id}", response_model=chat_schemas.Message)
async def message(
        message_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.get(session, model_id=message_id)
    return message_obj


@message_router.get("/{message_id}/user", response_model=user_schemas.UserRead)
async def message_user(
        message_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.get(session, model_id=message_id)
    return message_obj.user


@message_router.get("/{message_id}/chat", response_model=chat_schemas.Chat)
async def message_chat(
        message_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.get(session, model_id=message_id)
    return message_obj.chat


@message_router.post("", response_model=chat_schemas.Message)
async def create_message(
        message: chat_schemas.MessageCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.create_user(session, user_id=user.id, obj_in=message)
    return message_obj


@message_router.put("", response_model=chat_schemas.Message)
async def update_message(
        message_id: uuid.UUID,
        message: chat_schemas.MessageUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.get(session, model_id=message_id)
    updated_message_obj = await crud_message.update(session, db_obj=message_obj, obj_in=message)
    return updated_message_obj


@message_router.delete("", response_model=chat_schemas.Message)
async def delete_message(
        message_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.get(session, model_id=message_id)
    deleted_message_obj = await crud_message.delete(session, model_id=message_obj.id)
    return deleted_message_obj
