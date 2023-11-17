from datetime import datetime

from sqlalchemy.orm import Session

from core.models.models import PlayListInfo, User
from core.schemas.playlist_info import PlaylistInfoCreate
from routers.user.user_crud import get_user


def create_playlist(db: Session, playlist_create: PlaylistInfoCreate, current_user: User):
    db_playlist = PlayListInfo(
        owner=current_user.id,
        title=playlist_create.title,
        description=playlist_create.description,
        create_time=datetime.now(),
        hide=0,
    )
    db.add(db_playlist)
    db.commit()

    class Config:
        orm_mode = True


def get_playlist_list(db: Session, skip: int = 0, limit: int = 10, keyword: str = ''):
    _playlist_list = db.query(PlayListInfo).filter(PlayListInfo.hide == 0).order_by(PlayListInfo.id.desc())
    if keyword:
        search = '%%{}%%'.format(keyword)
        _playlist_list = _playlist_list.filter(
            PlayListInfo.title.ilike(search) |
            PlayListInfo.description.ilike(search) |
            PlayListInfo.owner.ilike(search)
            # | _playlist_list.join(PlayListInfo.playlist).any(PlayListInfo.title.ilike(search))
        )

    total = _playlist_list.count()
    playlist_list = _playlist_list.order_by(PlayListInfo.id.desc()).offset(skip).limit(limit).distinct().all()

    return total, playlist_list


def get_playlist(db: Session, playlist_id: int):
    return db.query(PlayListInfo).filter(PlayListInfo.id == playlist_id, PlayListInfo.hide == 0).first()


def delete_playlist(db: Session, playlist_id: int):
    db.query(PlayListInfo).filter(PlayListInfo.id == playlist_id).update({"hide": 1})
    db.commit()


def update_playlist(db: Session, db_playlist: PlayListInfo, playlist_update: PlaylistInfoCreate):
    db_playlist.title = playlist_update.title
    db_playlist.description = playlist_update.description

    db.add(db_playlist)
    db.commit()

    class Config:
        orm_mode = True
