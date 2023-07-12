from fastapi import APIRouter
from src.auth.router import *

router = APIRouter()

router.include_router(**auth_router)
router.include_router(**register_router)
router.include_router(**verify_router)
router.include_router(**reset_password_router)
router.include_router(**users_router)
