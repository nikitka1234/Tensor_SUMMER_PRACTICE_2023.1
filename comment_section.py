###############
# auth_router #
###############


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


###############
# chat_router #
###############


# @chat_router.put("/{chat_id}/tags")
# async def add_chat_tags(
#         chat_id: uuid.UUID,
#         tags_id: list[uuid.UUID],
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     for tag_id in tags_id:
#         chat_tags_obj = search_schemas.ChatTagsCreate(chat_id=chat_id, tags_id=tag_id)
#         await crud_chat_tags.create(session, obj_in=chat_tags_obj)

# @chat_router.delete("/{chat_id}/tags")
# async def delete_chat_tags(
#         chat_id: uuid.UUID,
#         tags_id: list[uuid.UUID],
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     for tag_id in tags_id:
#         chat_tags_obj = crud_chat_tags.get_by_parameters(session, chat_id=chat_id, tag_id=tag_id)
#         delete_chat_tags_obj = crud_user_chats.delete(session, model_id=chat_tags_obj.id)

# import uuid
#
# from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
# from fastapi.encoders import jsonable_encoder
# from fastapi.responses import HTMLResponse
# from sqlalchemy import insert
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from src.database import get_async_session
# from manager import manager

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


#################
# search_router #
#################


# @tag_router.post("", response_model=search_schemas.Tag)
# async def create_tag(
#         tag: search_schemas.TagCreate,
#         holder: Holder,
#         holder_id: uuid.UUID,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     tag_obj = await crud_tag.create(session, obj_in=tag)
#
#     if holder == Holder.user:
#         user_tags_create = search_schemas.UserTagsCreate(user_id=holder_id, tag_id=tag_obj.id)
#         await crud_user_tags.create(session, obj_in=user_tags_create)
#     elif holder == Holder.chat:
#         chat_tags_create = search_schemas.ChatTagsCreate(chat_id=holder_id, tag_id=tag_obj.id)
#         await crud_chat_tags.create(session, obj_in=chat_tags_create)
#
#     return tag_obj
#
#
# @tag_router.post("/user", response_model=list[search_schemas.Tag])
# async def create_user_tags(
#         tags: list[search_schemas.TagCreate],
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     tags_obj = []
#
#     for tag in tags:
#         tag_obj = await crud_tag.create(session, obj_in=tag)
#         user_tags_create = search_schemas.UserTagsCreate(user_id=user.id, tag_id=tag_obj.id)
#         await crud_user_tags.create(session, obj_in=user_tags_create)
#         tags_obj.append(tag_obj)
#
#     return tags_obj
#
#
# @tag_router.post("/chat", response_model=list[search_schemas.Tag])
# async def create_chat_tags(
#         tags: list[search_schemas.TagCreate],
#         chat_id: uuid.UUID,
#         user: User = Depends(current_user),
#         session: AsyncSession = Depends(get_async_session)
# ):
#     tags_obj = []
#
#     for tag in tags:
#         tag_obj = await crud_tag.create(session, obj_in=tag)
#         chat_tags_create = search_schemas.ChatTagsCreate(chat_id=chat_id, tag_id=tag_obj.id)
#         await crud_chat_tags.create(session, obj_in=chat_tags_create)
#         tags_obj.append(tag_obj)
#
#     return tags_obj
