from typing import AsyncGenerator
from config import USER, PASS, HOST, PORT, DB_Name

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from sqlalchemy import Column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL, TINYINT, TEXT, TIME, DATE, ENUM, VARCHAR, NCHAR, BOOLEAN

DATABASE_URL = f"mysql+aiomysql://{USER}:{PASS}@{HOST}:{PORT}/{DB_Name}"


class Base(DeclarativeBase):
    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(INTEGER(unsigned=True), primary_key=True)
    login = Column(VARCHAR(length=50), nullable=False, unique=True)
    hashed_password = Column(TEXT(), nullable=False)
    photo = Column(VARCHAR(length=20), nullable=False)
    name = Column(VARCHAR(length=40), nullable=False)
    s_name = Column(VARCHAR(length=40), nullable=False)
    b_day = Column(DATE(), nullable=False)
    gender = Column(ENUM("М", "Ж"), nullable=False)
    email = Column(VARCHAR(length=250), nullable=False, unique=True)
    is_active = Column(BOOLEAN(), nullable=False)
    is_superuser = Column(BOOLEAN(), nullable=False)
    is_verified = Column(BOOLEAN(), nullable=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
