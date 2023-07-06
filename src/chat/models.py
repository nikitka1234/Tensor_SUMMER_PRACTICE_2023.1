from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
from datetime import datetime

from src.database import Base


class Message(Base):
    __tablename__ = "message"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    text = Column(Text, nullable=False)
    sender_id = Column(UUID, ForeignKey("user.id"))
    recipient_id = Column(UUID, ForeignKey("user.id"))
    time = Column(TIMESTAMP, default=datetime.utcnow)

    sender = relationship("User", back_populates="message")
    recipient = relationship("User", back_populates="message")


class ChatParticipant(Base):
    __tablename__ = "chat_participant"
    chat_id = Column(UUID, ForeignKey("chat.id"))
    user_id = Column(UUID, ForeignKey("user.id"))

    chat = relationship("Chat", back_populates="participants")
    user = relationship("User", back_populates="participants")


class Chat(Base):
    __tablename__ = "chat"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)

    participants = relationship("ChatParticipant", back_populates="chat")
