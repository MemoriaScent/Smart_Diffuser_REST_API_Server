from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.models.models import User
from core.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user_create: UserCreate):
    db_user = User(
        stdId=user_create.stdId,
        password=pwd_context.hash(user_create.password),
        name=user_create.name,
        authority=1,
        hide=0,
    )
    db.add(db_user)
    db.commit()


def get_existing_user(db: Session, user_create: UserCreate):
    _db_user = db.query(User).filter(User.stdId == user_create.stdId, User.hide == 0).first()
    return


def get_user(db: Session, student_id: str):
    return db.query(User).filter(User.stdId == student_id, User.hide == 0).first()


def get_user_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    _user_list = db.query(User).filter(User.hide == 0).order_by(User.stdId.desc())
    if keyword:
        search = '%%{}%%'.format(keyword)
        _user_list = _user_list.filter(User.name.ilike(search) | User.stdId.ilike(search))

    total = _user_list.count()
    user_list = _user_list.order_by(User.id.desc()).offset(skip).limit(limit).distinct().all()

    return total, user_list


def delete_user(db: Session, student_id: str):
    db.query(User).filter(User.stdId == student_id).update({"hide": 1})
    db.commit()


def update_user(db: Session, db_user: User, user_update: UserUpdate, authority: int):
    #todo: 플레이리스 관련 수정 필요
    # 수정가능한 사용자 정보: 생성한 플레이리스트

    db_user.password = pwd_context.hash(user_update.password)

    if authority == 0:
        db_user.name = user_update.name
        db_user.authority = user_update.authority

    db.add(db_user)
    db.commit()
