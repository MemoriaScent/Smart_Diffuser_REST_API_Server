from enum import Enum

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.config import Config

import routers.user.user_crud as user_crud
from core.database import get_db

config = Config('.env')
SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DATABASE_URL')

ACCESS_TOKEN_EXPIRE_MINUTES = float(config('ACCESS_TOKEN_EXPIRE_MINUTES'))
SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


def get_current_user(token: str = Depends(oauth2_scheme),
                     db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        student_id: str = payload.get("sub")
        if student_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    else:
        student_id = user_crud.get_user(db, student_id=student_id)
        if student_id is None:
            raise credentials_exception
        return student_id


class Authority(Enum):
    Admin = 0
    User = 1
