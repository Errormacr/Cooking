import datetime
from pydantic import EmailStr
from typing import Optional
from fastapi_users import schemas
from pydantic import BaseModel


class UserRead(schemas.BaseUser[int]):
    login: str
    name: Optional[str] = None
    s_name: Optional[str] = None
    b_day: Optional[datetime.datetime] = None
    gender: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    login: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(BaseModel):
    login: str = None
    email: EmailStr = None
    name: Optional[str] = None
    s_name: Optional[str] = None
    b_day: Optional[datetime.datetime] = None
    gender: Optional[str] = None
