from pydantic import BaseModel, field_validator


class User(BaseModel):
    id: int
    stdId: str
    password: str
    name: str
    authority: int
    hide: int = 0

    class Token(BaseModel):
        access_token: str
        token_type: str
        student_id: str


class UserInformation(BaseModel):
    id: int
    stdId: str
    name: str
    authority: int


class UserCreate(BaseModel):
    stdId: str
    password: str
    name: str

    @field_validator('stdId', 'password', 'name')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

    @field_validator('stdId')
    def student_id_length(cls, v):
        if len(v) != 8:
            raise ValueError('학번은 8자리여야 합니다.')
        return v


class UserList(BaseModel):
    total: int = 0
    user_list: list[UserInformation] = []


class UserUpdate(UserCreate):
    user_id: int


class UserDelete(BaseModel):
    user_id: int
