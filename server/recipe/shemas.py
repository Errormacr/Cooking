from pydantic import BaseModel
import datetime
from typing import Optional, List
from fastapi import UploadFile


class Recipe_create(BaseModel):
    name: str
    servings_cout: int
    cook_time: int
    recommend: Optional[str] = None


class Recipe_update(BaseModel):
    name: Optional[str] = None
    servings_cout: Optional[int] = None
    cook_time: Optional[int] = None
    recommend: Optional[str] = None


class Step(BaseModel):
    description: str
    media: UploadFile
    timer: int
