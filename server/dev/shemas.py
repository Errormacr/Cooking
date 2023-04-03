from pydantic import BaseModel


class Ingredient_create(BaseModel):
    name: str
    unit_ID: int
    kkal: float
    belki: float
    zhiry: float
    uglevody: float
