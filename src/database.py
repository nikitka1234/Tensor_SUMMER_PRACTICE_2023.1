from typing import AsyncGenerator, TYPE_CHECKING

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from .config import database_settings

from .auth.models import User


# Указание echo=True при инициализации движка позволит нам увидеть сгенерированные SQL-запросы в консоли.
# Мы должны отключить поведение "expire on commit (завершить при фиксации)" для сессий с expire_on_commit=False.
# Это связано с тем, что в настройках async мы не хотим,
# чтобы SQLAlchemy выдавал новые SQL-запросы к базе данных при обращении к уже закоммиченным объектам.

engine = create_async_engine(database_settings.postgresql_url, future=True, echo=True)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False,
                                       autocommit=False, autoflush=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
