import datetime
from typing import Optional
from pydantic import condecimal, EmailStr
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import CHAR, ENUM, INTEGER, TINYINT, DECIMAL, TEXT, TIME, DATE
from sqlmodel import Field, SQLModel, create_engine, UniqueConstraint, CheckConstraint


class Recipe(SQLModel, table=True):
    __tablename__ = 'Recipe'
    __table_args__ = (UniqueConstraint("name"), UniqueConstraint("photo"), CheckConstraint('servings_cout>0'),)
    recipe_ID: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    photo: str = Field(max_length=50)
    servings_cout: int = Field(sa_column=Column(TINYINT(unsigned=True), nullable=False))
    cook_time: datetime.timedelta = Field(sa_column=(TIME(timezone=False)))
    rating: int = Field(sa_column=Column(INTEGER(unsigned=False), nullable=False))
    recommend: Optional[str] = Field(sa_column=(TEXT()))
    author: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="User.user_ID")


class Ingredient(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("name"),)
    ingredient_ID: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False, primary_key=True))
    name: str = Field(max_length=50)
    kkal: float = Field(sa_column=Column(DECIMAL(unsigned=True), nullable=False))
    belki: float = Field(sa_column=Column(DECIMAL(unsigned=True), nullable=False))
    zhiry: float = Field(sa_column=Column(DECIMAL(unsigned=True), nullable=False))
    uglevody: float = Field(sa_column=Column(DECIMAL(unsigned=True), nullable=False))


class Step(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("media"),)
    step_ID: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), default=None,
                                                    primary_key=True))
    description: str = Field(sa_column=Column(TEXT(), nullable=False))
    timer: Optional[datetime.timedelta] = Field(sa_column=Column(TIME(), nullable=True), default=None)
    media: Optional[str] = Field(max_length=20)
    recipe_ID: int = Field(foreign_key="Recipe.recipe_ID")


class Tag(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("name"),)
    tag_ID: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=20)


class User(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("login"), UniqueConstraint("mail"),)
    user_ID: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False, default=None,
                                                    primary_key=True))
    login: str = Field(max_length=50)
    password: str
    photo: str = Field(max_length=20)
    name: str = Field(max_length=40)
    s_name: str = Field(max_length=40)
    b_day: datetime.datetime = Field(sa_column=Column(DATE(), nullable=False))
    gender: str = Field(sa_column=Column(ENUM("М", "Ж")))
    mail: EmailStr


class Unit(SQLModel, table=True):
    __table_args__ = (UniqueConstraint("name"),)
    unit_ID: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False, default=None,
                                                    primary_key=True))
    name: str = Field(max_length=20)


class Recipe_ingredient(SQLModel, table=True):
    __table_args__ = (CheckConstraint("count>0"),)
    recipe_ID_ingredient: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False, default=None,
                                                                 primary_key=True))
    recipe_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Recipe.recipe_ID")
    ingredient_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False),
                               foreign_key="Ingredient.ingredient_ID")
    count: float = Field(sa_column=Column(DECIMAL(unsigned=True), nullable=False))
    unit_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Unit.unit_ID")


class Recipe_tag(SQLModel, table=True):
    recipe_ID_tag: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False, default=None,
                                                          primary_key=True))
    recipe_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Recipe.recipe_ID")
    tag_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Tag.tag_ID")


class Favourite_recipe(SQLModel, table=True):
    favourite_ID: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False, default=None,
                                                         primary_key=True))
    recipe_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Recipe.recipe_ID")
    unit_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Unit.unit_ID")


class Score_recipe(SQLModel, table=True):
    Score_ID: Optional[int] = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False, default=None,
                                                     primary_key=True))
    recipe_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Recipe.recipe_ID")
    unit_ID: int = Field(sa_column=Column(INTEGER(unsigned=True), nullable=False), foreign_key="Unit.unit_ID")
    score: int = Field(sa_column=Column(TINYINT(unsigned=True), nullable=False))


sqlite_file_name = "database.db"
sqlite_url = f"mysql+pymysql://root:pass@localhost:3306/Cooking"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
