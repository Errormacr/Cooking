from auth.db import get_async_session, User as auth_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Response
from sqlalchemy import select, insert, update, delete
from models import User, Favourite_recipe, Score_recipe, Recipe, Tag, Recipe_tag
from utils import fastapi_users
from auth.shemas import UserUpdate
from sqlalchemy import exc

router = APIRouter(prefix="/users")

current_user = fastapi_users.current_user()


@router.get("/", tags=["users"])
async def get_user(user_id: int = None, user_name: str = None, user_email: str = None,
                   session: AsyncSession = Depends(get_async_session)):
    if not user_id and not user_email and not user_name:
        raise HTTPException(status_code=400, detail={"error": "type id, login or mail"})
    if user_id:
        query = select(User).where(User.c.id == user_id)
        result = await session.execute(query)
        result = result.all()
    if result == [] and user_name:
        query = select(User).where(User.c.login == user_name)
        result = await session.execute(query)
        result = result.all()
    if not result and user_email:
        query = select(User).where(User.c.email == user_email)
        result = await session.execute(query)
        result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find user")
    result = {"id": result[0][0], "login": result[0][1], "photo": result[0][3], "email": result[0][5],
              "name": result[0][6], "s_name": result[0][7], "b_day": result[0][8], "gender": result[0][9],
              "is_active": result[0][10], "is_superuser": result[0][11], "is_verified": result[0][12]}
    return result


@router.get("/current/", tags=["users"])
async def get_current_user(user: auth_user = Depends(current_user),
                           session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.c.id == user.id)
    result = await session.execute(query)
    result = result.all()
    result = {"id": result[0][0], "login": result[0][1], "photo": result[0][3], "email": result[0][5],
              "name": result[0][6], "s_name": result[0][7], "b_day": result[0][8], "gender": result[0][9],
              "is_active": result[0][10], "is_superuser": result[0][11], "is_verified": result[0][12]}
    return result


@router.get("/photo", tags=["users"])
async def get_user_photo(user_id: int = None, user_name: str = None, user_email: str = None,
                         session: AsyncSession = Depends(get_async_session)):
    if not user_id and not user_email and user_name:
        raise HTTPException(status_code=400, detail={"error": "type id, login or mail"})
    if user_id:
        try:
            with open(f"../photo/user/{user_id}_user_photo", "rb") as photo:
                result = await session.execute(select(User.c.photo_type).where(User.c.id == user_id))
                result = result.all()
                if result:
                    data = photo.read()
                    return Response(data, status_code=200, media_type=result[0][0])
        except:
            pass
    if user_name:
        query = select(User).where(User.c.login == user_name)
        result = await session.execute(query)
        result = result.all()

    if not result and user_email:
        query = select(User).where(User.c.email == user_email)
        result = await session.execute(query)
        result = result.all()
    if user_id and not result:
        raise HTTPException(status_code=404, detail="can't find photo")
    if not result:
        raise HTTPException(status_code=404, detail="can't find user")
    result = result[0][0]
    try:
        with open(f"../photo/user/{result}_user_photo", "rb") as photo:
            result_type = await session.execute(select(User.c.photo_type).where(User.c.id == user_id))
            result_type = result_type.all()
            if result_type:
                data = photo.read()
                return Response(data, status_code=200, media_type=result_type[0][0])
            else:
                raise HTTPException(status_code=404, detail="can't find photo")
    except:
        raise HTTPException(status_code=404, detail="can't find photo")


@router.get("/current/photo", tags=["users"])
async def get_current_user_photo(user: auth_user = Depends(current_user),
                                 session: AsyncSession = Depends(get_async_session)):
    with open(f"../photo/user/{user.id}_user_photo", "rb") as photo:
        result = await session.execute(select(User.c.photo_type).where(User.c.id == user.id))
        result = result.all()
        if result:
            data = photo.read()
            return Response(data, status_code=200, media_type=result[0][0])
        else:
            raise HTTPException(status_code=404, detail="can't find photo")


@router.put("", status_code=201, tags=["users"])
async def update_user(photo: UploadFile = None, user_req: UserUpdate = Depends(),
                      user: auth_user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    b = False
    stmt = update(User)
    if photo is not None:
        cont = await photo.read()
        try:
            f = open(f"../photo/user/{user_id}_user_photo", "wb")
        except:
            raise HTTPException(status_code=404, detail="can't find photo")
        f.write(cont)
        await session.execute(update(User).where(User.c.id == user.id).values(photo_type=photo.content_type))
        await session.commit()
        f.close()
    if user_req.gender not in ('Ж', 'М'):
        raise HTTPException(status_code=400, detail="gender must be M or Ж")
    for key, value in user_req.__dict__.items():
        if value is not None:
            b = True
            stmt = stmt.values({key: value})
    if b:
        stmt = stmt.where(User.c.id == user.id)
        await session.execute(stmt)
    try:
        await session.commit()
        return user_req
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.get("/{user_id}/favourite", tags=["Favourite recipe"])
async def get_fav_recipe_of_user(user_id: int,
                                 session: AsyncSession = Depends(get_async_session)):
    query = select(Favourite_recipe.c.recipe_ID).where(Favourite_recipe.c.user_ID == user_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find favourite recipe")
    ans = []
    for rec in result:
        query = select(Recipe).where(Recipe.c.recipe_ID == rec[0])
        result_recipe = await session.execute(query)
        result_recipe = result_recipe.all()
        query = select(Recipe_tag.c.tag_ID).where(Recipe_tag.c.recipe_ID == rec[0])
        result_tag = await session.execute(query)
        result_tag = result_tag.all()
        tags = []
        for tag in result_tag:
            query = select(Tag.c.name).where(Tag.c.tag_ID == tag[0])
            result_tag_name = await session.execute(query)
            result_tag_name = result_tag_name.all()
            tags.append(result_tag_name[0][0])
        ans.append({
            "recipe_id": result_recipe[0][0],
            'recipe_desc': {"name": result_recipe[0][1], "photo": result_recipe[0][2],
                            "servings_cout": result_recipe[0][4], "cook_time": result_recipe[0][5],
                            "rating": result_recipe[0][6], "recommend": result_recipe[0][7],
                            "author": result_recipe[0][8]},
            "tags": tags})
    return ans


@router.post("/favourite", status_code=201, tags=["Favourite recipe"])
async def create_fav_recipe_of_user(recipe_id: int, user: auth_user = Depends(current_user),
                                    session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(insert(Favourite_recipe).values(user_ID=user.id, recipe_ID=recipe_id))
        await session.commit()
        return {"user_id": user.id, "recipe_id": recipe_id}
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.delete("/favourite", status_code=204, tags=["Favourite recipe"])
async def delete_fav_recipe_of_user(recipe_id: int, user: auth_user = Depends(current_user),
                                    session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Favourite_recipe).where(
        Favourite_recipe.c.user_ID == user.id).where(Favourite_recipe.c.recipe_ID == recipe_id)
    await session.execute(stmt)
    try:
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.post("/score/", status_code=201, tags=["Score"])
async def post_score(recipe_id: int, score: int, user: auth_user = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    try:
        await session.execute(insert(Score_recipe).values(user_ID=user.id, recipe_ID=recipe_id, score=score))
        await session.commit()

    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    return {"user_id": user.id, "recipe_id": recipe_id, "score": score}


@router.get("/score/", tags=["Score"])
async def get_score_of_recipe(recipe_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Score_recipe).where(Score_recipe.c.recipe_ID == recipe_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find score")
    r = [rec[3] for rec in result]
    r = sum(r)
    result = {"recipe_ID": recipe_id, "score": r}
    return result


@router.delete("/score/", status_code=204, tags=["Score"])
async def delete_score_of_recipe(recipe_id: int, user: auth_user = Depends(current_user),
                                 session: AsyncSession = Depends(get_async_session)):
    stmt = delete(Score_recipe).where(
        Score_recipe.c.user_ID == user.id and Score_recipe.c.recipe_ID == recipe_id)
    try:
        await session.execute(stmt)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    return


@router.put("/score/", tags=['Score'])
async def update_score(recipe_id: int, score: int, user: auth_user = Depends(current_user),
                       session: AsyncSession = Depends(get_async_session)):
    query = select(Score_recipe).where(Score_recipe.c.recipe_ID == recipe_id and Score_recipe.c.user_ID == user.id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail={"Error": "Can't find this score"})
    stmt = update(Score_recipe).where(
        Score_recipe.c.user_ID == user.id and Score_recipe.c.recipe_ID == recipe_id).values(score=score)
    try:
        await session.execute(stmt)
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})
    return {"user_ID": user.id, "recipe_ID": recipe_id, "score": score}
