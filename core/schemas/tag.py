from pydantic import BaseModel, field_validator


class TagInfo(BaseModel):
    id: int
    name: str


class TagInfoCreate(BaseModel):
    name: str

    @field_validator('name')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v


class TagList(BaseModel):
    tag_list: list[TagInfo] = []


class Tag(BaseModel):
    id: int
    recipe_id: int
    tag_id: int


class TagCreate(BaseModel):
    recipe_id: int
    tag_id: int


class AddTag(BaseModel):
    recipe_id: int
    tag_list: list[str] = []

    @field_validator('tag_list')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
