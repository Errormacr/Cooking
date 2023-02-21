from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    photo: str
    name: str
    s_name: str
    b_day: datetime.datetime
    gender: str
    email: EmailStr


class UserCreate(schemas.BaseUserCreate):
    login: str = Field(max_length=50)
    photo: str = Field(max_length=20)
    name: str = Field(max_length=40)
    s_name: str = Field(max_length=40)
    b_day: datetime.datetime = Field(sa_column=Column(DATE(), nullable=False))
    gender: str = Field(sa_column=Column(ENUM("М", "Ж")))
