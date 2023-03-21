from utils import fastapi_users
from auth.db import get_async_session, User as auth_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Header, Response, Form, Request
from sqlalchemy import select, insert, update, delete, exc, func
from operator import itemgetter
import json
import datetime
from pathlib import Path
from typing import List
from recipe.shemas import Recipe_create, Step, Recipe_update
from models import Recipe as Recipe_bd, Recipe_tag, User, Step as Step_bd, Ingredient, Recipe_ingredient, Tag, Unit

router = APIRouter(prefix="/recipes")

current_user = fastapi_users.current_user()


@router.post("/get/", tags=["recipe"])
async def get_recipe(tag: List[int] = None, name_sort: int = None, score_sort: int = None, time_sort: int = None,
                     ingredients: List[int] = None, author: int = None,ot_raiting: int = None, do_raiting: int = None,
                     ot_kkal: float = None, ot_belki: float = None, ot_zhiry: float = None, ot_uglevody: float = None,
                     do_kkal: float = None, do_belki: float = None, do_zhiry: float = None, do_uglevody: float = None,
                     author_name: str = None,
                     less_cook_time: int = None, more_cook_time: int = 0,
                     name: str = None,
                     offset: int = 0, limit: int = 10,
                     session: AsyncSession = Depends(get_async_session)):
    query = select(Recipe_bd)
    if tag is not None and tag != [0]:
        for i in tag:
            result = await session.execute(select(Recipe_tag.c.recipe_ID).where(Recipe_tag.c.tag_ID == i))
            result = [j[0] for j in result.all()]
            query = query.where(Recipe_bd.c.recipe_ID.in_(result))
    if ingredients is not None and ingredients != [0]:
        for i in ingredients:
            result = await session.execute(
                select(Recipe_ingredient.c.recipe_ID).where(Recipe_ingredient.c.ingredient_ID == i))
            result = [j[0] for j in result.all()]
            query = query.where(Recipe_bd.c.recipe_ID.in_(result))
    if author_name is not None:
        s = r"%{}%".format(str(author_name))
        result = await session.execute(select(User.c.id).where(User.c.login.ilike(s)))
        result = [i[0] for i in result.all()]
        query = query.where(Recipe_bd.c.author.in_(result))
    if author is not None:
        query = query.where(Recipe_bd.c.author == author)
    if ot_raiting:
        query = query.where(Recipe_bd.c.rating >= ot_raiting)
    if do_raiting:
        query = query.where(Recipe_bd.c.rating <= do_raiting)
    if less_cook_time is not None:
        query = query.where(Recipe_bd.c.cook_time < less_cook_time)
    if more_cook_time is not None:
        query = query.where(Recipe_bd.c.cook_time > more_cook_time)
    if name is not None:
        query = query.where(Recipe_bd.c.name.like("%" + name + "%"))
    if time_sort == 1:
        query = query.order_by(Recipe_bd.c.cook_time)
    elif time_sort == -1:
        query = query.order_by(Recipe_bd.c.cook_time.desc())
    elif score_sort == 1:
        query = query.order_by(Recipe_bd.c.rating)
    elif score_sort == -1:
        query = query.order_by(Recipe_bd.c.rating.desc())
    elif name_sort == 1:
        query = query.order_by(Recipe_bd.c.name)
    elif name_sort == -1:
        query = query.order_by(Recipe_bd.c.name.desc())
    query = query.offset(offset).limit(limit)
    result_rec = await session.execute(query)
    result_rec = result_rec.all()
    result = []
    if not result_rec:
        raise HTTPException(status_code=404, detail="Can't found recipe")
    if not ot_kkal and not ot_belki and not ot_zhiry and not ot_uglevody and not do_kkal and not do_belki and not do_zhiry and not do_uglevody:
        result = result_rec
    else:
        for i in result_rec:
            kkal = 0
            belki = 0
            zhiry = 0
            uglevody = 0
            query = select(Recipe_ingredient).where(Recipe_ingredient.c.recipe_ID == i[0])
            result_ingr_rec = await session.execute(query)
            result_ingr_rec = result_ingr_rec.all()
            for j in result_ingr_rec:
                query = select(Ingredient).where(Ingredient.c.ingredient_ID == j[2])
                result_ingr = await session.execute(query)
                result_ingr = result_ingr.all()
                kkal += result_ingr[0][3]
                belki += result_ingr[0][4]
                zhiry += result_ingr[0][5]
                uglevody += result_ingr[0][6]
            if ot_kkal:
                if kkal < ot_kkal:
                    continue
            if ot_belki:
                if belki < ot_belki:
                    continue
            if ot_zhiry:
                if zhiry < ot_zhiry:
                    continue
            if ot_uglevody:
                if uglevody < ot_uglevody:
                    continue
            if do_kkal:
                if kkal > do_kkal:
                    continue
            if do_belki:
                if belki > do_belki:
                    continue
            if do_zhiry:
                if zhiry > do_zhiry:
                    continue
            if do_uglevody:
                if uglevody > do_uglevody:
                    continue
            result.append(i)

    tags = {}
    for i in result:
        query = select(Recipe_tag.c.tag_ID).where(Recipe_tag.c.recipe_ID == i[0])
        result1 = await session.execute(query)
        result1 = result1.all()
        tags_rec = []
        for j in result1:
            query = select(Tag.c.name).where(Tag.c.tag_ID == j[0])
            resultTag = await session.execute(query)
            resultTag = resultTag.all()
            if resultTag:
                tags_rec.append(resultTag[0][0])
        tags[i[0]] = tags_rec
    answer = [{
        "recipe_id": rec[0],
        "name": rec[1], "photo": rec[2], "photo_type": rec[3], "servings_cout": rec[4], "cook_time": rec[5],
        "rating": rec[6], "recommend": rec[7], "author": rec[8],
        'tags': tags[rec[0]]} for rec in result]

    return answer


@router.get("/{recipe_id}", tags=["recipe"])
async def get_one_recipe(recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Recipe_bd).where(Recipe_bd.c.recipe_ID == recipe_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Not found recipe")
    tags = {}
    for i in result:
        query = select(Recipe_tag.c.tag_ID).where(Recipe_tag.c.recipe_ID == i[0])
        result1 = await session.execute(query)
        result1 = result1.all()
        tags_rec = []
        for j in result1:
            query = select(Tag.c.name).where(Tag.c.tag_ID == j[0])
            resultTag = await session.execute(query)
            resultTag = resultTag.all()
            if resultTag:
                tags_rec.append(resultTag[0][0])
        tags[i[0]] = tags_rec
    belky = 0
    zhiry = 0
    uglevody = 0
    kkal = 0
    ingredients = []
    for i in result:
        query = select(Recipe_ingredient).where(Recipe_ingredient.c.recipe_ID == i[0])
        result1 = await session.execute(query)
        result1 = result1.all()
        for j in result1:
            query = select(Ingredient).where(Ingredient.c.ingredient_ID == j[2])
            resultIngr = await session.execute(query)
            resultIngr = resultIngr.all()
            if resultIngr[0][2] in (1, 2):
                modif = j[3] / 100
                kkal += resultIngr[0][3] * modif
                belky += resultIngr[0][4] * modif
                zhiry += resultIngr[0][5] * modif
                uglevody += resultIngr[0][6] * modif
            else:
                modif = j[3]
                kkal += resultIngr[0][3] * modif
                belky += resultIngr[0][4] * modif
                zhiry += resultIngr[0][5] * modif
                uglevody += resultIngr[0][6] * modif
            resultUnit = await session.execute(select(Unit.c.name).where(Unit.c.unit_ID == resultIngr[0][2]))
            resultUnit = resultUnit.all()
            ingredients.append((resultIngr[0][1], resultUnit[0][0], j[3]))
    answer = [{
        "recipe_id": rec[0],
        'recipe_desc': {"name": rec[1], "photo": rec[2], "photo_type": rec[3], "servings_cout": rec[4],
                        "cook_time": rec[5],
                        "rating": rec[6], "recommend": rec[7], "author": rec[8]},
        'tags': tags[rec[0]],
        'ingredients': ingredients,
        'belky': belky, 'zhiry': zhiry, 'uglevody': uglevody, 'kkal': kkal} for rec in result]
    return answer


@router.post("/", status_code=201, tags=["recipe"])
async def create_recipe(photo: UploadFile, tag: str = None,
                        ingredients: str = None, recipe: Recipe_create = Depends(),
                        user: auth_user = Depends(current_user),
                        session: AsyncSession = Depends(get_async_session)):
    if tag:
        try:
            tag = list(tag.split(','))
        except:
            raise HTTPException(status_code=400, detail="Bad tags")
    if ingredients:
        try:
            ingredients = list(ingredients.split(','))
        except:
            raise HTTPException(status_code=400, detail="Bad ingredients")
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
                                    recommend=recipe.recommend, photo=f"/photo/recipe/0_recipe_photo.jpg",
                                    photo_type="qswdsa", rating=0,
                                    author=user.id)

    await session.execute(stmt)
    result = await session.execute(select(Recipe_bd.c.recipe_ID))
    r = max([i[0] for i in result.all()])
    stmt = update(Recipe_bd).where(Recipe_bd.c.recipe_ID == r).values(photo=f"/photo/recipe/{r}_recipe_photo",
                                                                      photo_type=photo.content_type)
    await session.execute(stmt)
    f = open(f"../photo/recipe/{r}_recipe_photo", "wb")
    cont = await photo.read()
    f.write(cont)
    f.close()
    if tag:
        for i in tag:
            stmt = insert(Recipe_tag).values(recipe_ID=r, tag_ID=int(i))
            await session.execute(stmt)
    if ingredients:
        for i in ingredients:
            ingredient, count = i.split('-')
            stmt = insert(Recipe_ingredient).values(recipe_ID=r, ingredient_ID=int(ingredient), count=float(count))
            await session.execute(stmt)
    try:
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    return recipe, r


@router.get("/photo/{recipe_id}", tags=["recipe"])
async def get_recipe_photo(recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        photo_path = Path(f"../photo/recipe/{recipe_id}_recipe_photo")
        result = await session.execute(select(Recipe_bd.c.photo_type).where(Recipe_bd.c.recipe_ID == recipe_id))
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="Can't find photo")
        with open(photo_path, "rb") as photo:
            data = photo.read()
            return Response(data, status_code=200, media_type=result[0][0])
    except:
        raise HTTPException(status_code=404, detail="Can't find photo")


@router.get("/{step_id}_media/", tags=["step"])
async def get_media_step(step_id: int):
    try:
        video_path = Path(f"../media/{step_id}_media")
        result = await session.execute(select(Step_bd.c.media_type).where(Step_bd.c.recipe_ID == step_id))
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="Can't find media")
        with open(video_path, "rb") as video:
            data = video.read()
            return Response(data, status_code=200, media_type=result[0][0])
    except:
        raise HTTPException(status_code=404, detail="Can't find media")


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
    stmt = update(Step_bd).where(Step_bd.c.step_ID == r).values(media=f"/media/{r}_media",
                                                                media_type=step.media.content_type)
    await session.execute(stmt)
    try:
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    f = open(f"../media/{r}_step", "wb")
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
    if recipe.name or recipe.servings_cout or recipe.cook_time or recipe.recommend:
        print(recipe)
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
        f = open(f"../photo/recipe/{recipe_id}_recipe_photo", "wb")
        cont = await photo.read()
        await session.execute(
            update(Recipe_bd).where(Recipe_bd.c.recipe_ID == recipe_id).values(photo_type=photo.content_type))
        await session.commit()
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
async def create_recipe_ingredient_relation(ingredient_id: int, recipe_id: int, count: float,
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
    result = [{"step_ID": rec[0], "description": rec[1], "timer": rec[2], "media": rec[3], "recipe_ID": rec[5]} for rec
              in result]
    return result


@router.put("/step/{step_id}", status_code=201, tags=["step"])
async def update_step_of_recipe(step_id: int, description: str = None,
                                timer: int = None,
                                media: UploadFile = None, user: auth_user = Depends(current_user),
                                session: AsyncSession = Depends(get_async_session)):
    if not description and not timer and not media:
        raise HTTPException(status_code=400, detail="Not enough data")
    recipe_id = await session.execute(select(Step_bd.c.recipe_ID).where(Step_bd.c.step_ID == step_id))
    recipe_id = recipe_id.all()
    if not recipe_id:
        raise HTTPException(status_code=404, detail="Can't find step")
    recipe_id = recipe_id[0][0]
    print(recipe_id)
    author = await session.execute(select(Recipe_bd.c.author).where(Recipe_bd.c.recipe_ID == recipe_id))
    author = author.all()
    if not author:
        raise HTTPException(status_code=404, detail="Can't find recipe")
    if author[0][0] != user.id:
        raise HTTPException(status_code=400, detail="User not author of this step")
    stmt = update(Step_bd).where(Step_bd.c.step_ID == step_id)
    if description:
        stmt = stmt.values(description=description)
    if timer:
        stmt = stmt.values(timer=timer)
    if media:
        media_file = open(f"../media/{step_id}_media", "wb")
        cont = await media.read()
        media_file.write(cont)
        stmt = stmt.values(media_type=media.content_type)
    try:
        await session.execute(stmt)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    return {"decription": description, "timer": timer, "media": media}
