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
@router.post("/tag_list", response_model=tag.TagList)
def create_tag(tag_list: tag.TagStrList, db: Session = Depends(get_db)):
    return {"tag_list": tag_crud.get_tag_info_list(db, tag_list.tag_list).tag_list}


