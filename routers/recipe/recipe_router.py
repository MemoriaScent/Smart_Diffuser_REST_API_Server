from datetime import timedelta, datetime
from typing import Optional, Annotated

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config
import hashlib
import json

from core.database import get_db
from core.models import models
from core.models.models import UserRecipe, UserRecipeUsePerfume
from core.schemas import recipe
from core.schemas import tag
from dependencies import get_current_user
import routers.recipe.recipe_crud as recipe_crud
import util.file_crud as file_crud

config = Config('.env')

router = APIRouter(
    prefix="/api/recipe",
    tags=["Recipe"]
)

# Todo 계정 관련하여 추가하여야 함.
# Create
@router.post("/", status_code=status.HTTP_200_OK)
async def create_recipe(new_recipe: str = Form(..., description='레시피 정보 Json 형식, set_id의 경우 옵션 new_recipe={"set_id": 0, "title": "string", "description": "string"}'),
                        file: UploadFile = File(None),
                        db: Session = Depends(get_db)
                        ):
    data = json.loads(new_recipe.replace("new_recipe=", ""))
    create_recipe = recipe.RecipeCreate(**data)

    file_id = None

    if file:
        file_id = await file_crud.create_file(db, file)

    try:
        return {"recipe": recipe_crud.create_recipe(db, file_id, create_recipe)}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                      detail=f"레시피 생성에 실패하였습니다. {e}")
