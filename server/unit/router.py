from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from models import Unit
from auth.db import get_async_session

router = APIRouter(prefix="/unit", tags=["unit"])


@router.get("/")
async def get_unit(unit_id: int = None, session: AsyncSession = Depends(get_async_session), offset: int = 0,
                   limit: int = 10):
    stmt = select(Unit)
    if unit_id:
        stmt = stmt.where(Unit.c.unit_ID == unit_id)
    stmt = stmt.offset(offset).limit(limit)
    result = await session.execute(stmt)
    result = result.all()
    result = [{"id": rec[0], "unit": rec[1]} for rec in result]
    if not result:
        raise HTTPException(status_code=404, detail="Can't found unit")
    return result
