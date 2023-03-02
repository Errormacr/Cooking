from auth.db import get_async_session, User as auth_user
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, insert, update, delete
from models import User, Favourite_recipe, Score_recipe
from utils import fastapi_users
from auth.shemas import UserUpdate

router = APIRouter(prefix="/users", tags=["users"])

current_user = fastapi_users.current_user()


@router.get("/{user_id}")
async def get_user(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(User).where(User.c.id == user_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find user")
    result = {"id": result[0][0], "login": result[0][1], "photo": result[0][3], "email": result[0][4],
              "name": result[0][5], "s_name": result[0][6], "b_day": result[0][7], "gender": result[0][8],
              "is_active": result[0][9], "is_superuser": result[0][10], "is_verified": result[0][11]}
    return result


@router.put("/{user_id}", status_code=201)
async def update_user(user_id: int, photo: UploadFile = None, user_req: UserUpdate = Depends(),
                      user: auth_user = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="User don't have permission")
    stmt = update(User)
    if photo is not None:
        cont = await photo.read()
        f = open(f"../photo/user/{user_id}_user_photo.jpg", "wb")
        f.write(cont)
        f.close()
    for key, value in user_req.__dict__.items():
        if value is not None:
            stmt = stmt.values({key: value})
    await session.execute(stmt)
    try:
        await session.commit()
        return user_req
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.get("/{user_id}/favourite")
async def get_fav_recipe_of_user(user_id: int, user: auth_user = Depends(current_user),
                                 session: AsyncSession = Depends(get_async_session)):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="User don't have permission")
    query = select(Favourite_recipe).where(Favourite_recipe.c.user_ID == user_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find favourite recipe")
    result = [{"recipe_ID": rec[1], "user_ID": rec[2]} for rec in result]
    return result


@router.post("/{user_id}/favourite", status_code=201)
async def create_fav_recipe_of_user(user_id: int, recipe_id: int, user: auth_user = Depends(current_user),
                                    session: AsyncSession = Depends(get_async_session)):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="User don't have permission")
    await session.execute(insert(Favourite_recipe).values(user_ID=user_id, recipe_ID=recipe_id))
    try:
        await session.commit()
        return {"user_id": user_id, "recipe_id": recipe_id}
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.delete("/{user_id}/favourite", status_code=204)
async def delete_fav_recipe_of_user(user_id: int, recipe_id: int, user: auth_user = Depends(current_user),
                                    session: AsyncSession = Depends(get_async_session)):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="User don't have permission")
    stmt = delete(Favourite_recipe).where(
        Favourite_recipe.c.user_ID == user_id and Favourite_recipe.c.recipe_ID == recipe_id)
    await session.execute(stmt)
    try:
        await session.commit()
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.post("/{user_id}/score", status_code=201)
async def post_score(user_id: int, recipe_id: int, score: int, user: auth_user = Depends(current_user),
                     session: AsyncSession = Depends(get_async_session)):
    if user_id != user.id:
        raise HTTPException(status_code=400, detail="User don't have permission")
    await session.execute(insert(Score_recipe).values(user_ID=user_id, recipe_ID=recipe_id, score=score))
    try:
        await session.commit()
        return {"user_id": user_id, "recipe_id": recipe_id, "score": score}
    except exc.IntegrityError:
        raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
    except exc.DataError:
        raise HTTPException(status_code=400, detail={"Error": "Data error"})


@router.get("/score/")
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


@router.delete("/{user_id}/score/", status_code=204)
async def get_score_of_recipe(user_id: int, recipe_id: int, user: auth_user = Depends(current_user),
                              session: AsyncSession = Depends(get_async_session)):
    if user_id == user.id:
        stmt = delete(Score_recipe).where(
            Score_recipe.c.user_ID == user_id and Score_recipe.c.recipe_ID == recipe_id)
        await session.execute(stmt)
        try:
            await session.commit()
        except exc.IntegrityError:
            raise HTTPException(status_code=400, detail={"Error": "Data error (Duplicate, foreign key)"})
        except exc.DataError:
            raise HTTPException(status_code=400, detail={"Error": "Data error"})
        return
    raise HTTPException(status_code=400, detail="User don't have permission")
