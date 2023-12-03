import uvicorn
from fastapi import (
    FastAPI,
)

from internal.admin import admin_router as admin
from internal.file import file_router as file
from routers.user import users_router as user
from routers.tag import tag_router as tag
from routers.recipe import recipe_router as recipe

app = FastAPI()

# internal
app.include_router(admin.router)
app.include_router(file.router)

# routers
app.include_router(user.router)
app.include_router(tag.router)
app.include_router(recipe.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{echo}")
async def echo(echo: str):
    return {"echo": echo}


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=80, workers=4)
