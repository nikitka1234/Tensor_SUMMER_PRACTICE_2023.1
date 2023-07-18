import uuid

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
# from src.main import app
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_async_session
from .manager import manager
from .models import Chat
from .schemas import ChatCreate, UserChatsCreate, MessageCreate, MessageUpdate
from .service import crud_chat, crud_message, crud_user_chats
from ..auth.models import User
from ..api.deps import current_user

from ..auth import schemas as user_schemas
from ..chat import schemas as chat_schemas
from ..search import schemas as search_schemas
from ..search.service import crud_chat_tags

router = APIRouter()


@router.get("", response_model=list[chat_schemas.Chat])
async def chats(offset: int = 0, limit: int = 100, user: User = Depends(current_user)):
    return user.chats[offset:offset+limit]


@router.get("/{chat_id}", response_model=chat_schemas.Chat)
async def chat(
        chat_id: uuid.UUID,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    return chat_obj


@router.get("/{chat_id}/messages", response_model=list[chat_schemas.Message])
async def chat_messages(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    return chat_obj.messages[offset:offset+limit]


@router.get("/{chat_id}/users", response_model=list[user_schemas.UserRead])
async def chat_users(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    return chat_obj.users[offset:offset+limit]


@router.get("/{chat_id}/tags", response_model=list[chat_schemas.Tag])
async def chat_tags(
        chat_id: uuid.UUID,
        offset: int = 0,
        limit: int = 100,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    return chat_obj.tags[offset:offset+limit]


@router.post("", response_model=chat_schemas.Chat)
async def create_chat(
        chat: chat_schemas.ChatCreate,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.create(session, obj_in=chat)

    for user_id in users_id:
        user_chats_obj = UserChatsCreate(user_id=user_id, chat_id=chat_obj.id)
        await crud_user_chats.create(session, obj_in=user_chats_obj)

    return chat_obj


@router.put("/{chat_id}", response_model=chat_schemas.Chat)
async def update_chat(
        chat_id: uuid.UUID,
        chat: chat_schemas.ChatUpdate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    updated_chat_obj = await crud_chat.update(session, db_obj=chat_obj, obj_in=chat)
    return updated_chat_obj


@router.put("/{chat_id}/users")
async def add_chat_users(
        chat_id: uuid.UUID,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    for user_id in users_id:
        user_chats_obj = UserChatsCreate(user_id=user_id, chat_id=chat_id)
        await crud_user_chats.create(session, obj_in=user_chats_obj)


@router.put("/{chat_id}/tags")
async def add_chat_tags(
        chat_id: uuid.UUID,
        tags_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    for tag_id in tags_id:
        chat_tags_obj = search_schemas.ChatTagsCreate(chat_id=chat_id, tags_id=tag_id)
        await crud_chat_tags.create(session, obj_in=chat_tags_obj)


@router.delete("/{chat_id}", response_model=chat_schemas.Chat)
async def delete_chat(
        chat_id: uuid.UUID, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    deleted_chat_obj = crud_chat.delete(session, model_id=chat_id)
    return deleted_chat_obj


@router.delete("/{chat_id}/users")
async def delete_chat_users(
        chat_id: uuid.UUID,
        users_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    for user_id in users_id:
        user_chats_obj = crud_user_chats.get_by_parameters(session, chat_id=chat_id, user_id=user_id)
        delete_user_chats_obj = crud_user_chats.delete(session, model_id=user_chats_obj.id)


@router.delete("/{chat_id}/tags")
async def delete_chat_users(
        chat_id: uuid.UUID,
        tags_id: list[uuid.UUID],
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    for tag_id in tags_id:
        chat_tags_obj = crud_chat_tags.get_by_parameters(session, chat_id=chat_id, tag_id=tag_id)
        delete_chat_tags_obj = crud_user_chats.delete(session, model_id=chat_tags_obj.id)


# @app.get("/")
# async def get():
#     return HTMLResponse(html)
#
#
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.send_personal_message(f"You wrote: {data}", websocket)
#             await manager.broadcast(f"Client #{client_id} says: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Client #{client_id} left the chat")
