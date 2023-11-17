from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

import internal.admin_crud as admin_crud
from core.database import get_db
from core.models import models
from dependencies import get_current_user, Authority

router = APIRouter(
    prefix="/api/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_user)]
)


# Authority 설정
# Create
@router.post("/authority", status_code=status.HTTP_204_NO_CONTENT)
async def create_authority(student_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.authority != Authority.Admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="권한이 없습니다.")

    admin_crud.set_authority(student_id=student_id, db=db)


# Read
@router.get("/authority/{student_id}")
async def get_user_authority_level(student_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.authority != Authority.Admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="권한이 없습니다.")

    return {"authority": Authority(admin_crud.get_authority(student_id=student_id, db=db)).name}


# Update
@router.put("/authority")
async def toggle_authority(student_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.authority != Authority.Admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="권한이 없습니다.")

    return {"message": f"Update Authority {admin_crud.toggle_authority(student_id=student_id, db=db)}"}


# Delete
@router.delete("/authority", status_code=status.HTTP_204_NO_CONTENT)
async def delete_authority(student_id: str, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.authority != Authority.Admin.value:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="권한이 없습니다.")
    admin_crud.unset_authority(student_id=student_id, db=db)
# !Authority 설정
