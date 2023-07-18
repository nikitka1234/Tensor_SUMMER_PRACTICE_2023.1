from typing import TYPE_CHECKING

from sqlalchemy import Text, DateTime, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

import uuid
from datetime import datetime

from src.base import Base
from .choices import ChatType, UserRole

if TYPE_CHECKING:
    from src.auth.models import User
    from src.search.models import Tag, ChatTags


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), nullable=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), nullable=False)
    external: Mapped[dict] = mapped_column(JSONB, nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="messages")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")


class UserChats(Base):
    __tablename__ = "user_chats"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("users.id"), primary_key=True, nullable=False)
    chat_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), primary_key=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(String(length=320), default=UserRole.user, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="user_chats_association")
    chat: Mapped["Chat"] = relationship("Chat", back_populates="user_chats_association")


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    type: Mapped[ChatType] = mapped_column(String(length=320), nullable=False)
    external: Mapped[dict] = mapped_column(JSONB, nullable=True)
    parent_id: Mapped[uuid.UUID] = mapped_column(UUID, ForeignKey("chats.id"), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    messages: Mapped[list["Message"]] = relationship("Message", back_populates="chat", lazy="selectin")
    users: Mapped[list["User"]] = relationship(secondary="user_chats", back_populates="chats", lazy="selectin")
    tags: Mapped[list["Tag"]] = relationship(secondary="chat_tags", back_populates="chats", lazy="selectin")

    user_chats_association: Mapped[list["UserChats"]] = relationship(back_populates="chat", viewonly=True)
    chat_tags_association: Mapped[list["ChatTags"]] = relationship(back_populates="chat", viewonly=True)
