import uuid

from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
# from src.main import app
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from .manager import manager
from .models import Chat
from .schemas import ChatCreate, UserChatsCreate
from .service import crud_chat, crud_message, crud_user_chats

router = APIRouter()


@router.post("/new_chat")
async def new_chat(chat: ChatCreate, users_id: list[uuid.UUID], session: AsyncSession = Depends(get_async_session)):
    chat_obj = await crud_chat.create(session, obj_in=chat)
    print(jsonable_encoder(chat_obj))

    for user in users_id:
        user = UserChatsCreate(user_id=user, chat_id=chat_obj.id)
        await crud_user_chats.create(session, obj_in=user)


@router.post("/add_chat_users")
async def add_chat_user(chat_id: uuid.UUID, users_id: list[uuid.UUID], session: AsyncSession = Depends(get_async_session)):
    for user in users_id:
        user = UserChatsCreate(user_id=user, chat_id=chat_id)
        await crud_user_chats.create(session, obj_in=user)


# html = """
# <!DOCTYPE html>
# <html>
#     <head>
#         <title>Chat</title>
#     </head>
#     <body>
#         <h1>WebSocket Chat</h1>
#         <h2>Your ID: <span id="ws-id"></span></h2>
#         <form action="" onsubmit="sendMessage(event)">
#             <input type="text" id="messageText" autocomplete="off"/>
#             <button>Send</button>
#         </form>
#         <ul id='messages'>
#         </ul>
#         <script>
#             var client_id = Date.now()
#             document.querySelector("#ws-id").textContent = client_id;
#             var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
#             ws.onmessage = function(event) {
#                 var messages = document.getElementById('messages')
#                 var message = document.createElement('li')
#                 var content = document.createTextNode(event.data)
#                 message.appendChild(content)
#                 messages.appendChild(message)
#             };
#             function sendMessage(event) {
#                 var input = document.getElementById("messageText")
#                 ws.send(input.value)
#                 input.value = ''
#                 event.preventDefault()
#             }
#         </script>
#     </body>
# </html>
# """
#
#
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
