from .auth import auth_backend
from .schemas import UserRead, UserCreate, UserUpdate

from src.api.deps import fastapi_users

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
