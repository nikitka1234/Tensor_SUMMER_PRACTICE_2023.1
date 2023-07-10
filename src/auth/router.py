import uuid

from fastapi_users import FastAPIUsers

from .auth import auth_backend
from .manager import get_user_manager
from .models import User
from .schemas import UserRead, UserCreate, UserUpdate

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

auth_router = {
    "router": fastapi_users.get_auth_router(auth_backend),
    "prefix": "/auth/jwt",
    "tags": ["auth"]
}

register_router = {
    "router": fastapi_users.get_register_router(UserRead, UserCreate),
    "prefix": "/auth",
    "tags": ["auth"]
}

verify_router = {
    "router": fastapi_users.get_verify_router(UserRead),
    "prefix": "/auth",
    "tags": ["auth"]
}

reset_password_router = {
    "router": fastapi_users.get_reset_password_router(),
    "prefix": "/auth",
    "tags": ["auth"]
}

users_router = {
    "router": fastapi_users.get_users_router(UserRead, UserUpdate),
    "prefix": "/users",
    "tags": ["users"]
}
