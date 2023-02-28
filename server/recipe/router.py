import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi_users import FastAPIUsers
from auth.db import get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from utils import fastapi_users
from recipe.shemas import Recipe_create
from models import Recipe as Recipe_bd, Recipe_tag

router = APIRouter(prefix="/recipes", tags=["recipes"])

current_user = fastapi_users.current_user()


@router.get("/")
async def get_recipe(tag: int = None, author: int = None, cook_time: datetime.timedelta = None, name: str = None,
                     offset: int = 0, limit: int = 10,
                     session: AsyncSession = Depends(get_async_session)):
    query = select(Recipe_bd)
    if tag is not None:
        result = await session.execute(select(Recipe_tag.c.recipe_ID).where(Recipe_tag.c.tag_ID == tag))
        r = result.all()
        r = [i[0] for i in r]
        query = query.where(Recipe_bd.c.recipe_ID.in_(r))
    if author is not None:
        query = query.where(Recipe_bd.c.author == author)
    if cook_time is not None:
        query = query.where(Recipe_bd.c.cook_time == cook_time)
    if name is not None:
        query = query.where(Recipe_bd.c.name == name)
    query = query.offset(offset).limit(limit)
    result = await session.execute(query)
    r = result.all()
    a = {
        f"{rec[0]}": {"name": f"{rec[1]}", "photo": f"{rec[2]}", "servings_cout": f"{rec[3]}", "cook_time": f"{rec[4]}",
                      "rating": f"{rec[5]}", "recommend": f"{rec[6]}", "author": f"{rec[7]}"} for rec in r}
    return a


@router.post("/")
async def create_recipe(recipe: Recipe_create, tag: List[int], user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)) -> Recipe_create:
    if recipe.servings_cout <= 0:
        raise HTTPException(status_code=400, detail="servings <= 0")
    if not recipe.name or not recipe.photo or not recipe.servings_cout or not recipe.cook_time:
        raise HTTPException(status_code=400, detail="Missing data")

    stmt = insert(Recipe_bd).values(**recipe.dict(), rating=0, author=user.id)
    await session.execute(stmt)
    await session.commit()

    result = await session.execute(select(Recipe_bd.c.recipe_ID))
    r = max([i[0] for i in result.all()])

    for i in tag:
        stmt = insert(Recipe_tag).values(recipe_ID=r, tag_ID=i)
        await session.execute(stmt)
        await session.commit()
    return recipe
