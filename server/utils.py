
from fastapi_users import FastAPIUsers
from auth.db import User
from auth.user_manager import get_user_manager
from auth.auth import auth_backend


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)