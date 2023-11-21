from typing import Annotated

import uvicorn
from fastapi import (
    Cookie,
    FastAPI,
    Query,
    WebSocket,
    WebSocketException,
    WebSocketDisconnect,
    status,
)
from fastapi.responses import HTMLResponse

from internal import admin
from routers.user import users_router as user

app = FastAPI()

# internal
app.include_router(admin.router)

# routers
app.include_router(user.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/{echo}")
async def echo(echo: str):
    return {"echo": echo}


if __name__ == "__main__":
    uvicorn.run(app='main:app', host="0.0.0.0", port=80, workers=4)
