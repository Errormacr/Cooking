from utils import fastapi_users
from auth.db import get_async_session, User as auth_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Header, Response, Form
from sqlalchemy import select, insert, update, delete, exc
import json
import datetime
from pathlib import Path
from typing import List
from recipe.shemas import Recipe_create, Step, Recipe_update
from models import Recipe as Recipe_bd, Recipe_tag, User, Step as Step_bd, Ingredient, Recipe_ingredient

router = APIRouter(prefix="/recipes")

current_user = fastapi_users.current_user()


@router.get("/", tags=["recipe"])
async def get_recipe(tag: int = None, author: int = None, author_name: str = None,
                     less_cook_time: int = None, more_cook_time: int = 0,
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
    if not result:
        raise HTTPException(status_code=404,detail="Can't found recipe")
    answer = [{
        "recipe_id": rec[0],
        'recipe_desc': {"name": rec[1], "photo": rec[2], "servings_cout": rec[3], "cook_time": rec[4],
                        "rating": rec[5], "recommend": rec[6], "author": rec[7]}} for rec in result]
    return answer


@router.get("/{recipe_id}", tags=["recipe"])
async def get_one_recipe(recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Recipe_bd).where(Recipe_bd.c.recipe_ID == recipe_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Not found recipe")
    answer = [{
        "recipe_id": rec[0],
        'recipe_desc': {"name": rec[1], "photo": rec[2], "servings_cout": rec[3], "cook_time": rec[4],
                        "rating": rec[5], "recommend": rec[6], "author": rec[7]}} for rec in result]
    return answer


@router.post("/", status_code=201, tags=["recipe"])
async def create_recipe(photo: UploadFile, tag: List[int or None] = list([0]), recipe: Recipe_create = Depends(),
                        user: auth_user = Depends(current_user),
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
    try:
        tag.remove(0)
    except:
        pass
    for i in tag:
        stmt = insert(Recipe_tag).values(recipe_ID=r, tag_ID=i)
        await session.execute(stmt)
    try:
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    return recipe, r


@router.get("/photo/{recipe_id}", tags=["recipe"])
async def get_recipe_photo(recipe_id: int):
    photo_path = Path(f"../photo/recipe/{recipe_id}_recipe_photo.jpg")
    with open(photo_path, "rb") as photo:
        data = photo.read()
        return Response(data, status_code=200, media_type="image/jpeg")


@router.get("/{step_id}_media/", tags=["step"])
async def get_media_step(step_id: int):
    video_path = Path(f"../media/{step_id}_media.mp4")
    with open(video_path, "rb") as video:
        data = video.read()
        return Response(data, status_code=200, media_type="video/mp4")


@router.post("/{recipe_id}/step", status_code=201, tags=["step"])
async def create_step(recipe_id: int, user: auth_user = Depends(current_user),
                      session: AsyncSession = Depends(get_async_session),
                      step: Step = Depends()):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = insert(Step_bd).values(description=step.description, timer=step.timer, media="", recipe_ID=recipe_id)
    await session.execute(stmt)
    result = await session.execute(select(Step_bd.c.step_ID))
    r = max([i[0] for i in result.all()])
    stmt = update(Step_bd).where(Step_bd.c.step_ID == r).values(media=f"/media/{r}_step.mp4")
    await session.execute(stmt)
    try:
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    f = open(f"../media/{r}_step.mp4", "wb")
    cont = await step.media.read()
    f.write(cont)
    f.close()


@router.delete("/{recipe_id}/tag", status_code=204, tags=["tag recipe"])
async def delete_tag_recipe(recipe_id: int, tag_id: int, user: auth_user = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = delete(Recipe_tag).where(Recipe_tag.c.recipe_ID == recipe_id and Recipe_tat.c.tag_ID == tag_id)
    await session.execute(stmt)
    try:
        await session.commit()
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"error": "tag error data"})


@router.delete("/{recipe_id}/ingredient", status_code=204, tags=["ingredient recipe"])
async def delete_ingredient_recipe(recipe_id: int, ingredient_id: int, user: auth_user = Depends(current_user),
                                   session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = delete(Recipe_ingredient).where(
        Recipe_ingredient.c.recipe_ID == recipe_id and Recipe_ingredient.c.ingredient_ID == ingredient_id)
    await session.execute(stmt)
    try:
        await session.commit()
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"error": "ingredient error data"})


@router.delete("/{recipe_id}/step", status_code=204, tags=["step"])
async def delete_step_recipe(recipe_id: int, step_id: int, user: auth_user = Depends(current_user),
                             session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = delete(Step_bd).where(
        Step_bd.c.recipe_ID == recipe_id and Step_bd.c.step_ID == step_id)
    await session.execute(stmt)
    try:
        await session.commit()
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"error": "step error data"})


@router.post("/{recipe_id}/tag", status_code=201, tags=["tag recipe"])
async def create_tag_recipe(recipe_id: int, tag_id: int, user: auth_user = Depends(current_user),
                            session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = insert(Recipe_tag).values(recipe_ID=recipe_id, tag_ID=tag_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"error": "tag error data"})
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"error": "tag error data (duplicate)"})


@router.put("/{recipe_id}", status_code=201, tags=["recipe"])
async def update_recipe(recipe_id: int, recipe: Recipe_update = Depends(),
                        photo: UploadFile = None,
                        user: auth_user = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = update(Recipe_bd)
    for key, value in recipe.__dict__.items():
        if value is not None:
            stmt = stmt.values({key: value})
    try:
        await session.execute(stmt)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    if photo is not None:
        f = open(f"../photo/recipe/{recipe_id}_recipe_photo.jpg", "wb")
        cont = await photo.read()
        f.write(cont)
        f.close()
    return recipe


@router.delete("/{recipe_id}", status_code=204, tags=["recipe"])
async def delete_recipe(recipe_id: int, user: auth_user = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    author = await session.execute(stmt)
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = delete(Recipe_bd).where(Recipe_bd.c.recipe_ID == recipe_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.post("{recipe_id}/{ingredient_id}", status_code=201, tags=["ingredient recipe"])
async def create_recipe_ingredient_relation(ingredient_id: int, recipe_id: int, count: int,
                                            user: auth_user = Depends(current_user),
                                            session: AsyncSession = Depends(get_async_session)):
    if count <= 0:
        raise HTTPException(status_code=400, detail="Count <= 0")
    stmt = select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id)
    recipe = await session.execute(stmt)
    recipe = recipe.all()
    if not recipe:
        raise HTTPException(status_code=404, detail="Not found recipe")
    if recipe[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author")
    stmt = insert(Recipe_ingredient).values(recipe_ID=recipe_id,
                                            ingredient_ID=ingredient_id,
                                            count=count)
    try:
        await session.execute(stmt)
        await session.commit()
        return dict(recipe_ID=recipe_id, ingredient_ID=ingredient_id, count=count)
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.get("/{recipe_id}/steps", tags=["step"])
async def get_steps_of_recipe(recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Step_bd).where(Step_bd.c.recipe_ID == recipe_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find steps")
    result = [{"step_ID": rec[0], "description": rec[1], "timer": rec[2], "media": rec[3], "recipe_ID": rec[4]} for rec
              in result]
    return result
