from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy import select, insert, update, delete
from models import Ingredient, Recipe_ingredient, Unit
from auth.db import get_async_session

router = APIRouter(prefix="/ingredient", tags=["ingredient"])


@router.get("/")
async def get_ingredients(recipe_id: int = None, ingredient_name: str = None, limit: int = 10, offset: int = 0,
                          session: AsyncSession = Depends(get_async_session)):
    if recipe_id:
        query = select(Recipe_ingredient).where(Recipe_ingredient.c.recipe_ID == recipe_id)
        if limit > 0:
            query = query.limit(limit)
        result = await session.execute(query)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="Can't find ingredients")
        ans = []
        for rec in result:
            query = select(Ingredient).where(Ingredient.c.ingredient_ID == rec[2])
            result_ingr = await session.execute(query)
            result_ingr = result_ingr.all()
            if ingredient_name:
                if ingredient_name not in result_ingr[0][1]:
                    continue
            print(result_ingr)
            if result_ingr[0][2] in (1, 2):
                kkal = rec[3] / 100 * result_ingr[0][3]
                belki = rec[3] / 100 * result_ingr[0][4]
                zhiry = rec[3] / 100 * result_ingr[0][5]
                uglevody = rec[3] / 100 * result_ingr[0][6]
            else:
                kkal = rec[3] * result_ingr[0][3]
                belki = rec[3] * result_ingr[0][4]
                zhiry = rec[3] * result_ingr[0][5]
                uglevody = rec[3] * result_ingr[0][6]
            query = select(Unit.c.name).where(Unit.c.unit_ID == result_ingr[0][2])
            result_unit = await session.execute(query)
            result_unit = result_unit.all()
            ans.append(
                {"id": rec[2], "name": result_ingr[0][1], "unit": result_unit[0][0], "count": rec[3], "kkal": kkal,
                 "belki": belki, "zhiry": zhiry, "uglevody": uglevody})
        if ans == []:
            raise HTTPException(status_code=404, detail="Can't find ingredients")
        return ans
    elif ingredient_name:
        query = select(Ingredient).where(Ingredient.c.name.like("%" + ingredient_name + "%"))
        if limit > 0:
            query = query.limit(limit)
        result = await session.execute(query)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="Can't find ingredients")
        ans = []
        for rec in result:
            query = select(Unit.c.name).where(Unit.c.unit_ID == rec[2])
            resultUnit = await session.execute(query)
            resultUnit = resultUnit.all()
            ans.append({"name": rec[1], "unit": resultUnit[0][0], "kkal": rec[3], "belki": rec[4], "zhiry": rec[5],
                        "uglevody": rec[6]})
        return ans
    else:
        query = select(Ingredient).offset(offset)
        if limit > 0:
            query = query.limit(limit)
        result = await session.execute(query)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="Can't find ingredients")
        result = [{"id": rec[0], "name": rec[1], "unit_id": rec[2], "kkal": rec[3], "belki": rec[4], "zhiry": rec[5],
                   "uglevody": rec[6]} for rec in result]
        return result


@router.get("/{ingredient_id}")
async def get_ingredient(ingredient_id: int = None, session: AsyncSession = Depends(get_async_session)):
    query = select(Ingredient).where(Ingredient.c.ingredient_ID == ingredient_id)
    result = await session.execute(query)
    result = result.all()
    if not result:
        raise HTTPException(status_code=404, detail="Can't find ingredient")
    result = {"id": result[0][0], "name": result[0][1], "unit_id": result[0][2], "kkal": result[0][3],
              "belki": result[0][4], "zhiry": result[0][5], "uglevody": result[0][6]}
    return result
