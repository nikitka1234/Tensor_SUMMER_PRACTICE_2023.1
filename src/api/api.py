from src.main import app
from src.auth import router


app.include_router(**router.auth_router)
app.include_router(**router.register_router)
app.include_router(**router.verify_router)
app.include_router(**router.reset_password_router)
app.include_router(**router.users_router)
