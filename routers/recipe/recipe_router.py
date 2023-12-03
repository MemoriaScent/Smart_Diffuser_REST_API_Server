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

config = Config('.env')

router = APIRouter(
    prefix="/api/recipe",
    tags=["Recipe"]
)

# Todo 계정 관련하여 추가하여야 함.
# Create
@router.post("/", status_code=status.HTTP_204_NO_CONTENT,
             description='new_recipe는 다음과 같이 입력해주세요. new_recipe={"set_id": 0, "title": "string", "description": "string"}')
async def create_recipe(new_recipe: str = Form(...),
                        file: UploadFile = File(None),
                        db: Session = Depends(get_db)
                        ):
    data = json.loads(new_recipe.replace("new_recipe=", ""))
    create_recipe = recipe.RecipeCreate(**data)

    if file:
        file_name = (hashlib.sha256(
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{file.filename}".encode())
                     .hexdigest() + "." + file.filename.split('.')[-1])

        file_location = f"./static/img/recipe/"

        # 파일 경로가 없다면 생성
        import os
        if not os.path.exists(os.path.dirname(file_location)):
            os.makedirs(file_location)

        file_location = os.path.join(file_location,file_name)
        async with aiofiles.open(file_location, 'wb+') as f:
            while content := await file.read(1024):
                await f.write(content)
    else:
        file_location = None

    recipe_crud.create_recipe(db, file_location, create_recipe)
