import uuid

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.crud_base import CRUDBase
from src.auth.models import User
from src.auth.schemas import (
    UserCreate,
    UserUpdate
)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


crud_user = CRUDUser(User)
