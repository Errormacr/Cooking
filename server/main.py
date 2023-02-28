from fastapi import FastAPI, Depends

from auth.shemas import UserRead, UserCreate
from auth.auth import auth_backend
from recipe.router import router as recipe_router
from utils import fastapi_users

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(recipe_router)
