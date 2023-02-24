import datetime

from  pydantic import EmailStr
from typing import Optional
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    login: str
    name: str
    s_name: str
    b_day: datetime.datetime
    gender: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    login: str
    photo: str
    name: str
    s_name: str
    b_day: datetime.datetime
    gender: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    pass