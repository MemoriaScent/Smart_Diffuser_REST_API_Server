import datetime

from fastapi import UploadFile
from pydantic import BaseModel, field_validator


class File(BaseModel):
    id: int
    file_path: str
    type: str
    original_name: str
    create: datetime.datetime


class FileCreate(BaseModel):
    file_path: str
    type: str
    original_name: str

    @field_validator('file_path', 'type', 'original_name')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

