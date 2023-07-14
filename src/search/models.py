from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from datetime import datetime

from src.base import Base

if TYPE_CHECKING:
    from src.auth.models import User
    from src.chat.models import Chat


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("categories.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    category: Mapped["Category"] = relationship("Category", back_populates="tags")
    users: Mapped[list["User"]] = relationship("User", secondary="user_tags", back_populates="tags")
    chats: Mapped[list["Chat"]] = relationship("Chat", secondary="chat_tags", back_populates="tags")


class UserTags(Base):
    __tablename__ = "user_tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("tags.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="user_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="user_tags")


class ChatTags(Base):
    __tablename__ = "chat_tags"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), nullable=False)
    tag_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("tags.id"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="chat_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="chat_tags")


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(length=320), unique=True, nullable=False)
    external: Mapped[dict] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    tags: Mapped[list["Tag"]] = relationship("Tag", back_populates="category")
