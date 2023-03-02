from pydantic import BaseModel
import datetime
from typing import Optional, List
from fastapi import UploadFile
from sqlalchemy.dialects.mysql import INTEGER, DECIMAL, TINYINT, TEXT, TIME, DATE, ENUM, VARCHAR, NCHAR, BOOLEAN


class Ingredient_create(BaseModel):
    name: str
    unit_ID: int
    kkal: float
    belki: float
    zhiry: float
    uglevody: float
