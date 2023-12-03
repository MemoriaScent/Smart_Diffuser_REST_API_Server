import urllib.parse

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from starlette import status

import internal.admin.admin_crud as admin_crud
from core.database import get_db
from core.models import models
from internal.file import file_crud

router = APIRouter(
    prefix="/api/file",
    tags=["File"]
)


# File
# Create
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_file(file: UploadFile = File(None), db: Session = Depends(get_db)):
    await file_crud.create_file(db=db, file=file)


# Read
@router.get("/{file_id}")
async def get_file(file_id: int, db: Session = Depends(get_db)):
    db_file = file_crud.get_file(db=db, file_id=file_id)

    def iter_file():
        with open(db_file.file_path, mode="rb") as f:
            yield from f

    return StreamingResponse(iter_file(), media_type=db_file.type,
                             headers={
                                 "Content-Disposition": f"attachment; filename={urllib.parse.quote(db_file.original_name, encoding='utf-8')}"}
                             )

@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    file_crud.delete_file(db=db, file_id=file_id)
