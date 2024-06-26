from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

import routers.tag.tag_crud as tag_crud
from core.database import get_db
from core.models import models
from core.schemas import tag
from dependencies import get_current_user
from routers.user.user_crud import pwd_context

config = Config('.env')

router = APIRouter(
    prefix="/api/tag",
    tags=["Tag"]
)


# Create
@router.post("/add_tag", status_code=status.HTTP_204_NO_CONTENT)
def add_tag(_add_tag: tag.AddTag, db: Session = Depends(get_db)):
    tag_crud.add_tag(db, _add_tag)


@router.post("/tag_list", response_model=tag.TagList)
def get_tag_id(tag_list: tag.TagStrList, db: Session = Depends(get_db)):
    return {"tag_list": tag_crud.get_tag_info_list(db, tag_list.tag_list)}


@router.delete("/{recipe_id}/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(recipe_id: int, tag_id: int, db: Session = Depends(get_db)):
    tag_crud.delete_tag(db, recipe_id, tag_id)