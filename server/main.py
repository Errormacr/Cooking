from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from auth.shemas import UserRead, UserCreate
from auth.auth import auth_backend
from recipe.router import router as recipe_router
from tag.router import router as tag_router
from ingredients.router import router as ingredient_router
from auth.router import router as user_router
from dev.router import router as dev_router
from unit.router import router as unit_router
from utils import fastapi_users

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
app.include_router(tag_router)
app.include_router(ingredient_router)
app.include_router(user_router)
app.include_router(dev_router)
app.include_router(unit_router)
