from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.models import models
from core.models.models import UserRecipe, UserRecipeUsePerfume
from core.schemas.recipe import RecipeCreate
from datetime import datetime


def get_recipe(db: Session, user_id: int, title: str):
    return db.query(UserRecipe).filter(UserRecipe.user_id == user_id, UserRecipe.title == title).first()


def create_recipe(db: Session, image_id: int, recipe_create: RecipeCreate, current_user: models.User | None = None):
    db_recipe = get_recipe(db, user_id=1, title=recipe_create.title)

    if db_recipe:
        raise ValueError('이미 존재하는 레시피입니다.')

    db_recipe = UserRecipe(
        user_id=1,
        set_id=recipe_create.set_id,
        title=recipe_create.title,
        description=recipe_create.description,
        image_id=image_id,
        create_time=datetime.now(),
    )
    db.add(db_recipe)
    db.commit()

    return get_recipe(user_id=1, title=recipe_create.title, db=db)

