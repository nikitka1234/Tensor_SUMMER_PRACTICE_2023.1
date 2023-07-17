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

router = APIRouter()


@router.post("/new_chat", response_model=chat_schemas.Chat)
async def new_chat(
        chat: ChatCreate, users_id: list[uuid.UUID], session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.create(session, obj_in=chat)

    for user in users_id:
        user_chats_create = UserChatsCreate(user_id=user, chat_id=chat_obj.id)
        await crud_user_chats.create(session, obj_in=user_chats_create)

    return chat_obj


@router.post("/add_chat_users")
async def add_chat_user(
        chat_id: uuid.UUID, users_id: list[uuid.UUID], session: AsyncSession = Depends(get_async_session)
):
    for user in users_id:
        user_chats_create = UserChatsCreate(user_id=user, chat_id=chat_id)
        await crud_user_chats.create(session, obj_in=user_chats_create)


@router.post("delete_chat_users")
async def delete_chat_users(
        chat_id: uuid.UUID, users_id: list[uuid.UUID], session: AsyncSession = Depends(get_async_session)
):
    for user in users_id:
        user_chats_create = UserChatsCreate(user_id=user, chat_id=chat_id)
        await crud_user_chats.delete(session, obj_in=user_chats_create)


@router.post("/update_chat", response_model=chat_schemas.Chat)
async def update_chat(
        chat_id: uuid.UUID, chat: chat_schemas.ChatUpdate, session: AsyncSession = Depends(get_async_session)
):
    chat_obj = await crud_chat.get(session, model_id=chat_id)
    updated_chat_obj = await crud_chat.update(session, db_obj=chat_obj, obj_in=chat)

    return updated_chat_obj


@router.post("/delete_chat", response_model=chat_schemas.Chat)
async def delete_chat(chat_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    deleted_chat_obj = await crud_chat.delete(session, model_id=chat_id)

    return deleted_chat_obj


@router.get("/chat", response_model=chat_schemas.Chat)
async def chat(chat_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    chat_obj = await crud_chat.get(session, model_id=chat_id)

    return chat_obj


@router.get("/chat_users", response_model=list[user_schemas.UserRead])
async def chat_users(chat_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    chat_obj = await crud_chat.get(session, model_id=chat_id)

    return chat_obj.users


@router.get("/chat_tags", response_model=list[search_schemas.Tag])
async def chat_tags(chat_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    chat_obj = await crud_chat.get(session, model_id=chat_id)

    return chat_obj.tags


@router.get("/chat_messages", response_model=list[chat_schemas.Message])
async def chat_messages(chat_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    chat_obj = await crud_chat.get(session, model_id=chat_id)

    return chat_obj.messages


@router.post("/add_message", response_model=chat_schemas.Message)
async def add_message(
        message: MessageCreate, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)
):
    message.user_id = user.id
    return await crud_message.create(session, obj_in=message)


@router.post("/update_message", response_model=chat_schemas.Message)
async def update_message(
        message_id: uuid.UUID, message: MessageUpdate, session: AsyncSession = Depends(get_async_session)
):
    message_obj = await crud_message.get(message_id)
    updated_message_obj = await crud_message.update(session, db_obj=message_obj, obj_in=message)

    return updated_message_obj


@router.post("/delete_message", response_model=chat_schemas.Message)
async def delete_message(message_id: uuid.UUID, session: AsyncSession = Depends(get_async_session)):
    message_obj = await crud_message.delete(session, model_id=message_id)

    return message_obj


@router.get("/user_chats", response_model=list[chat_schemas.Chat])
async def all_chats(user: User = Depends(current_user)):
    return [chat for chat in user.chats if not chat.deleted_at]


@router.get("all_user_messages", response_model=list[chat_schemas.Message])
async def all_user_messages(user: User = Depends(current_user)):
    return [message for message in user.messages if not chat.deleted_at]


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
