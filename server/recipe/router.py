import datetime
import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi_users import FastAPIUsers
from auth.db import get_async_session, User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from utils import fastapi_users
from recipe.shemas import Recipe_create, Step, Recipe_update
from models import Recipe as Recipe_bd, Recipe_tag, User, Step as Step_bd
from sqlalchemy.dialects.mysql import TIME

router = APIRouter(prefix="/recipes", tags=["recipes"])

current_user = fastapi_users.current_user()


@router.get("/")
async def get_recipe(tag: int = None, author: int = None, author_name: str = None,
                     less_cook_time: datetime.timedelta = None, more_cook_time: datetime.timedelta = 0,
                     name: str = None,
                     offset: int = 0, limit: int = 10,
                     session: AsyncSession = Depends(get_async_session)):
    query = select(Recipe_bd)
    if tag is not None:
        result = await session.execute(select(Recipe_tag.c.recipe_ID).where(Recipe_tag.c.tag_ID == tag))
        result = [i[0] for i in result.all()]
        query = query.where(Recipe_bd.c.recipe_ID.in_(result))
    if author_name is not None:
        s = r"%{}%".format(str(author_name))
        result = await session.execute(select(User.c.id).where(User.c.login.ilike(s)))
        result = [i[0] for i in result.all()]
        query = query.where(Recipe_bd.c.author.in_(result))
    if author is not None:
        query = query.where(Recipe_bd.c.author == author)
    if less_cook_time is not None:
        query = query.where(Recipe_bd.c.cook_time < less_cook_time)
    if more_cook_time is not None:
        query = query.where(Recipe_bd.c.cook_time > more_cook_time)
    if name is not None:
        query = query.where(Recipe_bd.c.name.like("%" + name + "%"))
    query = query.offset(offset).limit(limit)
    result = await session.execute(query)
    result = result.all()
    answer = [{
        "recipe_id": rec[0],
        'recipe_desc': {"name": rec[1], "photo": rec[2], "servings_cout": rec[3], "cook_time": rec[4],
                        "rating": rec[5], "recommend": rec[6], "author": rec[7]}} for rec in result]
    return answer


@router.get("/{recipe_id}")
async def get_one_recipe(recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Recipe_bd).where(Recipe_bd.c.recipe_ID == recipe_id)
    result = await session.execute(query)
    result = result.all()
    answer = [{
        "recipe_id": rec[0],
        'recipe_desc': {"name": rec[1], "photo": rec[2], "servings_cout": rec[3], "cook_time": rec[4],
                        "rating": rec[5], "recommend": rec[6], "author": rec[7]}} for rec in result]
    return answer


@router.post("/",status_code=201)
async def create_recipe(photo: UploadFile, tag: List[int] = 0, recipe: Recipe_create = Depends(),
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    if recipe.servings_cout <= 0:
        raise HTTPException(status_code=400, detail="servings <= 0")
    if not recipe.name or not recipe.servings_cout or not recipe.cook_time:
        raise HTTPException(status_code=400, detail="Missing data")
    query = select(Recipe_bd).where(Recipe_bd.c.name == recipe.name)
    result = await session.execute(query)
    result = result.all()
    if len(result) > 0:
        raise HTTPException(status_code=400, detail="duplicate name of recipe")

    stmt = insert(Recipe_bd).values(name=recipe.name, servings_cout=recipe.servings_cout,
                                    cook_time=recipe.cook_time,
                                    recommend=recipe.recommend, photo=f"/photo/recipe/0_recipe_photo.jpg", rating=0,
                                    author=user.id)
    await session.execute(stmt)
    result = await session.execute(select(Recipe_bd.c.recipe_ID))
    r = max([i[0] for i in result.all()])
    stmt = update(Recipe_bd).where(Recipe_bd.c.recipe_ID == r).values(photo=f"/photo/recipe/{r}_recipe_photo.jpg")
    await session.execute(stmt)
    f = open(f"../photo/recipe/{r}_recipe_photo.jpg", "wb")
    cont = await photo.read()
    f.write(cont)
    f.close()
    await session.commit()
    tag.remove(0)
    for i in tag:
        stmt = insert(Recipe_tag).values(recipe_ID=r, tag_ID=i)
        await session.execute(stmt)
        await session.commit()
    return recipe, r


@router.post("/{recipe_id}/step",status_code=201)
async def create_step(recipe_id: int, user: User = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session),
                      step: Step = Depends()):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = insert(Step_bd).values(description=step.description, timer=step.timer, media="", recipe_ID=recipe_id)
    await session.execute(stmt)
    await session.commit()
    result = await session.execute(select(Step_bd.c.step_ID))
    r = max([i[0] for i in result.all()])
    stmt = update(Step_bd).where(Step_bd.c.step_ID == r).values(media=f"/media/{r}_step.mp4")
    await session.execute(stmt)
    await session.commit()
    f = open(f"../media/{r}_step.mp4", "wb")
    cont = await step.media.read()
    f.write(cont)
    f.close()


@router.put("/{recipe_id}",status_code=201)
async def update_recipe(recipe_id: int, recipe: Recipe_update = Depends(), photo: UploadFile = None,
                        user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = update(Recipe_bd)
    if recipe.name is not None:
        stmt = stmt.values(name=recipe.name).where(Recipe_bd.c.recipe_ID == recipe_id)
    if recipe.servings_cout is not None:
        stmt = stmt.values(servings_cout=recipe.servings_cout).where(Recipe_bd.c.recipe_ID == recipe_id)
    if recipe.cook_time is not None:
        stmt = stmt.values(cook_time=recipe.cook_time).where(Recipe_bd.c.recipe_ID == recipe_id)
    if recipe.recommend is not None:
        stmt = stmt.values(recommend=recipe.recommend).where(Recipe_bd.c.recipe_ID == recipe_id)
    if recipe.name is not None or recipe.servings_cout is not None or recipe.cook_time is not None or recipe.recommend is not None:
        await session.execute(stmt)
        await session.commit()
    if photo is not None:
        f = open(f"../photo/recipe/{recipe_id}_recipe_photo.jpg", "wb")
        cont = await photo.read()
        f.write(cont)
        f.close()
    return recipe


@router.delete("/{recipe_id}",status_code=204)
async def delete_recipe(recipe_id: int, user: User = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = delete(Recipe_bd).where(Recipe_bd.c.recipe_ID == recipe_id)
    await session.execute(stmt)
    await session.commit()

