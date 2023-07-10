import uuid

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    email: EmailStr
    password: str
    is_active: bool | None = True
    is_superuser: bool | None = False
    is_verified: bool | None = False


class UserUpdate(schemas.BaseUserUpdate):
    password: str | None
    email: EmailStr | None
    is_active: bool | None
    is_superuser: bool | None
    is_verified: bool | None
