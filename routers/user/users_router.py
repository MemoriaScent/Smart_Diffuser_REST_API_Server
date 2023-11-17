from datetime import timedelta, datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

import routers.user.user_crud as user_crud
from core.database import get_db
from core.models import models
from core.schemas import user
from dependencies import get_current_user
from routers.user.user_crud import pwd_context

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

ACCESS_TOKEN_EXPIRE_MINUTES = float(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")

router = APIRouter(
    prefix="/api/user",
    tags=["user"]
)


# User
# Create
@router.post("/register", status_code=status.HTTP_204_NO_CONTENT)
def create_users(_user_create: user.UserCreate, db: Session = Depends(get_db)):
    user_data = user_crud.get_existing_user(db, user_create=_user_create)
    if user_data:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="이미 존재하는 사용자입니다.")
    user_crud.create_user(db, _user_create)


# Read
@router.get("/list", response_model=user.UserList)
async def read_users(page: int = 0, size: int = 10, db: Session = Depends(get_db), search: str = ''):

    total, _user_list = user_crud.get_user_list(db, skip=page*size, limit=size, keyword=search)

    return {
        "total": total,
        "user_list": _user_list
    }



@router.get("/me", response_model=user.UserInformation)
def read_current_user(current_user: models.User = Depends(get_current_user), db=Depends(get_db)):
    # Todo : 생성한 플레이리스트 정보 추가
    user_data = user_crud.get_user(db, student_id=current_user.stdId)

    return {
        "id": user_data.id,
        "stdId": user_data.stdId,
        "name": user_data.name,
        "authority": user_data.authority,
    }


@router.get("/{student_id}", response_model=user.UserInformation)
async def read_user(student_id: str, db=Depends(get_db)):
    # Todo : 생성한 플레이리스트 정보 추가
    user_data = user_crud.get_user(db, student_id=student_id)

    return {
        "id": user_data.id,
        "stdId": user_data.stdId,
        "name": user_data.name,
        "authority": user_data.authority,
    }


# Update
@router.put("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_user(_user_update: user.UserUpdate,
                      db: Session = Depends(get_db),
                        current_user: models.User = Depends(get_current_user)):
    # Todo : 특정 사용자의 정보를 수정하는 API
    # 수정가능한 사용자 정보: 이름, 권한, 생성한 플레이리스트, 비밀번호
    # 비밀번호는 암호화된 상태로 저장되어야 함
    # 이름과 권한은 관리자만 수정 가능
    db_user = user_crud.get_user(db, student_id=_user_update.stdId)

    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if current_user.id != db_user.user.id and current_user.authority != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")

    user_crud.update_user(db=db, db_user=db_user, user_update=_user_update, authority=current_user.authority)


# Delete
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(student_id: str, current_user: models.User = Depends(get_current_user), db=Depends(get_db)):
    db_user = user_crud.get_user(db, student_id=student_id)

    if current_user.id != student_id and current_user.authority != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")

    user_crud.delete_user(db=db, student_id=student_id)


# User Login
@router.post("/login", response_model=user.User.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                           db: Session = Depends(get_db)):

    # check user and password
    user_data = user_crud.get_user(db, form_data.username)
    if not user_data or not pwd_context.verify(form_data.password, user_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # make access token
    data = {
        "sub": user_data.stdId,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    access_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "student_id": user_data.stdId
    }
