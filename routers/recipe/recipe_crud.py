from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.models import models
from core.models.models import UserRecipe, UserRecipeUsePerfume
from core.schemas.recipe import RecipeCreate
from datetime import datetime


def create_recipe(db: Session, image_url: str, recipe_create: RecipeCreate, current_user: models.User | None = None):
    db_recipe = UserRecipe(
        user_id=1,
        set_id=recipe_create.set_id,
        title=recipe_create.title,
        description=recipe_create.description,
        image_url=image_url,
        create_time=datetime.now(),
    )
    db.add(db_recipe)
    db.commit()

