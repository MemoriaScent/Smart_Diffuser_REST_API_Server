import hashlib
from datetime import datetime

import aiofiles
from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.models.models import File


FILE_LOCATION = f"./static/img/recipe/"


def create_hash_name(file_name: str):
    return hashlib.sha256(
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{file_name}".encode()
    ).hexdigest()


def get_file(db: Session, file_id: int):
    return db.query(File).filter(File.id == file_id).first()


def get_file_by_original_name(db: Session, original_name: str):
    return db.query(File).filter(File.original_name == original_name).first()


async def create_file(db: Session, file: UploadFile):
    file_name = create_hash_name(file.filename)

    # 파일 경로가 없다면 생성
    import os

    if not os.path.exists(os.path.dirname(FILE_LOCATION)):
        os.makedirs(FILE_LOCATION)

    file_location = os.path.join(FILE_LOCATION, file_name)
    async with aiofiles.open(file_location, 'wb+') as f:
        while content := await file.read(1024):
            await f.write(content)

    # 파일 권한 변경
    os.chmod(file_location, 0o444)

    db_file = File(
        file_path=file_location,
        type=file.content_type,
        original_name=file.filename,
    )

    db.add(db_file)
    db.commit()

    return get_file_by_original_name(db=db, original_name=file.filename).id


def delete_file(db: Session, file_id: int):
    db.query(File).filter(File.id == file_id).delete()
    db.commit()




