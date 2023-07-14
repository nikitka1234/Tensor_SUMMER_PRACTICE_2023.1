from src.api.crud_base import CRUDBase
from .models import User
from .schemas import (
    UserCreate,
    UserUpdate
)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


crud_user = CRUDUser(User)
