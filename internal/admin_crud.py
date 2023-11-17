from sqlalchemy.orm import Session

from core.models.models import User


def set_authority(db: Session, student_id: str):
    db.query(User).filter(User.stdId == student_id).update({"authority": 0})
    db.commit()


def unset_authority(db: Session, student_id: str):
    db.query(User).filter(User.stdId == student_id).update({"authority": 1})
    db.commit()


def get_authority(db: Session, student_id: str):
    return db.query(User).filter(User.stdId == student_id).first().authority


def toggle_authority(db: Session, student_id: str):
    authority = get_authority(db, student_id)
    if authority == 0:
        unset_authority(db, student_id)
    else:
        set_authority(db, student_id)
    db.commit()

    return get_authority(db, student_id)

