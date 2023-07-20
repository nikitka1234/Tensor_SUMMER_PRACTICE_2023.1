import uuid

from fastapi_users import schemas
from pydantic import EmailStr

from datetime import datetime

from ..search.schemas import Tag


class UserRead(schemas.BaseUser[uuid.UUID]):
    # created_at: datetime
    # updated_at: datetime
    # deleted_at: datetime | None = None
    # last_login: datetime
    external: dict | None = None

    # tags: list[Tag]


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False
    external: dict | None = None


class UserUpdate(schemas.BaseUserUpdate):
    password: str | None
    email: EmailStr | None
    is_active: bool | None
    is_superuser: bool | None
    is_verified: bool | None
    external: dict | None = None
