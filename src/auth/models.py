from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB

from datetime import datetime

from src.base import Base

if TYPE_CHECKING:
    from src.chat.models import Message, UserChats
    from src.search.models import UserTags


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    last_login: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    external: Mapped[dict] = mapped_column(JSONB, nullable=True)

    # full_name: Mapped[str] = mapped_column(String(length=320))
    # birth_date: Mapped[date] = mapped_column(Date)
    # photo: Mapped[str] = mapped_column(String(length=320))
    # description: Mapped[str] = mapped_column(String(length=1024))
    # status: Mapped[str] = mapped_column(String(length=320))
    # emoji_status: Mapped[str | None] = mapped_column(String(length=64))

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="user")
    user_chats: Mapped[list["UserChats"]] = relationship("UserChats", back_populates="user")
    user_tags: Mapped[list["UserTags"]] = relationship("UserTags", back_populates="user")
