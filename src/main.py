from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.base import Base
from src.base_init import *

from src.auth.router import router as auth_router
from src.chat.router import chat_router, message_router
from src.search.router import category_router, tag_router


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
app.include_router(chat_router)
app.include_router(message_router)
app.include_router(category_router)
app.include_router(tag_router)


