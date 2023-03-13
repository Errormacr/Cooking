from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, insert, update, delete
from models import Tag, Recipe_tag
from auth.db import get_async_session, User
from utils import fastapi_users

router = APIRouter(prefix="/tag", tags=["tag"])

current_user = fastapi_users.current_user()


@router.get("/")
async def get_tags(recipe_id: int = None, limit: int = 10, offset: int = 0,
                   session: AsyncSession = Depends(get_async_session)):
    if recipe_id is None:
        query = select(Tag).offset(offset)
        if limit > 0:
            query = query.limit(limit)
        result = await session.execute(query)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="Can't find tags")
        result = [{"id": rec[0], "name": rec[1]} for rec in result]
        return result
    else:
        query = select(Recipe_tag).where(Recipe_tag.c.recipe_ID == recipe_id).offset(offset)
        if limit > 0:
            query = query.limit(limit)
        result = await session.execute(query)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="Can't find tags")
        ans = []
        for rec in result:
            query = select(Tag.c.name).where(Tag.c.tag_ID == rec[2])
            result_tag = await session.execute(query)
            result_tag = result_tag.all()
            ans.append({"recipe_id": rec[0], "tag_id": rec[2], "name": result_tag[0][0]})
        return ans


@router.get("/{tag_id}")
async def get_tag(tag_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Tag).where(Tag.c.tag_ID == tag_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find tag")
    result = {"id": result[0][0], "name": result[0][1]}
    return result


@router.post("/", status_code=201)
async def create_tag(tag: str, user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
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


@router.delete("/", status_code=204)
async def delete_tag(tag_id: int, user: User = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(delete(Tag).where(Tag.c.tag_ID == tag_id))
        await session.commit()
    except exc.DataError:
        return {"Error": "Data error"}
