from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .base import Base
from .base_init import *

from src.api.api import router as auth_router
from src.chat.router import router as chat_router
from src.search.router import router as  search_router

app = FastAPI(
    title="Tensor_SUMMER_PRACTICE_2023.1"
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router, prefix="/chats", tags=["/chats"])
app.include_router(search_router, prefix="/search", tags=["/search"])
