from utils import fastapi_users
from auth.db import get_async_session, User as auth_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, insert, update, delete
from sqlalchemy import exc
import json
import datetime
import keyring
from typing import List
from dev.shemas import Ingredient_create
from models import Tag, Ingredient, Unit

router = APIRouter(prefix="/dev", tags=["dev"])

current_user = fastapi_users.current_user()


@router.post("/ingredient/", status_code=201,tags=["ingredient"])
async def create_ingredient(ingredient: Ingredient_create, key: str,
                            session: AsyncSession = Depends(get_async_session)):
    if key != keyring.get_password("Cooking", "DEV"):
        raise HTTPException(status_code=400, detail="Wrong key")
    try:
        await session.execute(insert(Ingredient).values(**ingredient.dict()))
        await session.commit()
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Diplicate"})
    return ingredient


@router.post("/unit/", status_code=201,tags=["unit"])
async def create_unit(unit: str, key: str, session: AsyncSession = Depends(get_async_session)):
    if key != keyring.get_password("Cooking", "DEV"):
        raise HTTPException(status_code=400, detail="Wrong key")
    try:
        await session.execute(insert(Unit).values(name=unit))
        await session.commit()
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Diplicate"})

    return {"unit": unit}


@router.post("/tag/", status_code=201,tags=["tag"])
async def create_tag(tag: str, key: str, session: AsyncSession = Depends(get_async_session)):
    if key != keyring.get_password("Cooking", "DEV"):
        raise HTTPException(status_code=400, detail="Wrong key")
    if len(tag) > 20:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    try:
        await session.execute(insert(Tag).values(name=tag))
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Diplicate"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    return {"tag": tag}


@router.delete("/tag/", status_code=204,tags=["tag"])
async def delete_tag(key: str, tag_id: int, session: AsyncSession = Depends(get_async_session)):
    if key != keyring.get_password("Cooking", "DEV"):
        raise HTTPException(status_code=400, detail={"Error": "Wrong key"})
    try:
        await session.execute(delete(Tag).where(Tag.c.tag_ID == tag_id))
        await session.commit()
    except exc.DataError:
        return {"Error": "Data error"}


@router.delete("/ingredient/", status_code=204,tags=["ingredient"])
async def delete_ingredient(key: str, ingredient_id: int, session: AsyncSession = Depends(get_async_session)):
    if key != keyring.get_password("Cooking", "DEV"):
        raise HTTPException(status_code=400, detail={"Error": "Wrong key"})
    try:
        await session.execute( delete(Ingredient).where(Ingredient.c.tag_ID == ingredient_id))
        await session.commit()
    except exc.DataError:
        return {"Error": "Data error"}


@router.delete("/unit/", status_code=204,tags=["unit"])
async def delete_unit(key: str, unit_id: int, session: AsyncSession = Depends(get_async_session)):
    if key != keyring.get_password("Cooking", "DEV"):
        raise HTTPException(status_code=400, detail={"Error": "Wrong key"})
    try:
        await session.execute( delete(Unit).where(Unit.c.unit_ID == unit_id))
        await session.commit()
    except exc.DataError:
        return {"Error": "Data error"}