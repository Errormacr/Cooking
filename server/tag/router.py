from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, insert, update, delete
from models import Tag, Recipe_tag
from auth.db import get_async_session

router = APIRouter(prefix="/tag", tags=["tag"])


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
        result = [{"recipe_id": rec[0], "tag_id": rec[2]} for rec in result]
        return result


@router.get("/{tag_id}")
async def get_tag(tag_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Tag).where(Tag.c.tag_ID == tag_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find tag")
    result = {"id": result[0][0], "name": result[0][1]}
    return result
