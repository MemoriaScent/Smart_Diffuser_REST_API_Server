import datetime

from fastapi import UploadFile
from pydantic import BaseModel, field_validator


class Recipe(BaseModel):
    id: int
    set_id: int | None
    user_id: int
    title: str
    description: str
    image_url: str
    create_time: datetime.datetime


class RecipeCreate(BaseModel):
    set_id: int | None = None
    title: str
    description: str

    @field_validator('title', 'description')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class RecipeUsePerfume(BaseModel):
    id: int
    recipe_id: int
    cartridge_id: int
    count: int


class RecipeUsePerfumeCreate(BaseModel):
    recipe_id: int
    cartridge_id: int
    count: int
