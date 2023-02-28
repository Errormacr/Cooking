from pydantic import BaseModel
import datetime
from typing import Optional


class Recipe_create(BaseModel):
    name: str
    photo: bytes
    servings_cout: int
    cook_time: datetime.timedelta
    recommend: Optional[str] = None
