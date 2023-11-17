from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from core.database import get_db
from core.schemas import playlist_info
from routers.user.playlist import playlist_crud
from dependencies import get_current_user
from core.models import models

router = APIRouter(
    prefix="/api/playlist",
    tags=["playlist"],
)


# Playlist_info
# Create
@router.post("/", status_code=status.HTTP_204_NO_CONTENT)
async def create_playlist(_playlist_create: playlist_info.PlaylistInfoCreate,
                          db=Depends(get_db),
                          current_user: models.User = Depends(get_current_user)):
    playlist_crud.create_playlist(db, _playlist_create, current_user)


# Read
@router.get("/list", response_model=playlist_info.PlaylistList)
async def read_playlist_list(page: int = 0,
                             size: int = 10,
                             db=Depends(get_db),
                             search: str = ''):
    total, _playlist_list = playlist_crud.get_playlist_list(db, skip=page * size, limit=size, keyword=search)
    return {"total": total, "playlist_list": _playlist_list}


@router.get("/{playlist_id}", response_model=playlist_info.PlayListInfo)
async def read_playlist(playlist_id: str, db=Depends(get_db)):
    playlist_data = playlist_crud.get_playlist(playlist_id=int(playlist_id), db=db)

    if not playlist_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")

    return {
        "id": playlist_data.id,
        "owner": playlist_data.owner,
        "title": playlist_data.title,
        "description": playlist_data.description,
        "create_time": playlist_data.create_time,
    }


# Update
@router.put("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_playlist(_update_playlist: playlist_info.PlaylistUpdate,
                          db=Depends(get_db),
                          current_user: models.User = Depends(get_current_user)):
    db_playlist = playlist_crud.get_playlist(playlist_id=_update_playlist.playlist_id, db=db)

    if not db_playlist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if db_playlist.owner != current_user.id and current_user.authority != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="수정 권한이 없습니다.")

    playlist_crud.update_playlist(db, db_playlist, _update_playlist)


# Delete
@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_playlist(playlist_id: str, current_user: models.User = Depends(get_current_user), db=Depends(get_db)):
    db_playlist = playlist_crud.get_playlist(playlist_id=int(playlist_id), db=db)
    
    if not db_playlist:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    if db_playlist.owner != current_user.id and current_user.authority != 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="삭제 권한이 없습니다.")

    playlist_crud.delete_playlist(db, playlist_id=int(playlist_id))

# !Playlist_info
