from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
import config
from sqlalchemy.dialects.mysql import ENUM, DATE
from sqlmodel import Field

DATABASE_URL = f"mysql+pymysql://{config.USER}:{config.PASS}@{config.HOST}:{config.PORT}/{config.DB_Name}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    login: str = Field(max_length=50)
    photo: str = Field(max_length=20)
    name: str = Field(max_length=40)
    s_name: str = Field(max_length=40)
    b_day: datetime.datetime = Field(sa_column=Column(DATE(), nullable=False))
    gender: str = Field(sa_column=Column(ENUM("М", "Ж")))


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
