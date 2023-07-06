from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid
from datetime import datetime

from src.database import Base

# from src.auth.models import


class Photo(Base):
    __tablename__ = "photo"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    created_date = Column(TIMESTAMP, default=datetime.utcnow)
    profile_id = Column(UUID, ForeignKey("profile.id"))

    profile = relationship("Profile", back_populates="photos")


class Interest(Base):
    __tablename__ = "interest"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    interest = Column(String(100), nullable=False)
    profile_id = Column(UUID, ForeignKey("profile.id"))

    profile = relationship("Profile", back_populates="interests")


class Profile(Base):
    __tablename__ = "profile"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("user.id"))
    description = Column(String(500))
    status = Column(String(50))
    created_date = Column(TIMESTAMP, default=datetime.utcnow)
    last_update = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="profile")
    photos = relationship("Photo", back_populates="profile")
    interests = relationship("Interest", back_populates="profile")
