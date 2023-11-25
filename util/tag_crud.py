from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.models.models import User
from core.schemas.tag import TagInfo, Tag, TagInfoCreate, TagList, TagCreate, AddTag

# 하나의 유저 레시피에 추가 할 수 있는 태긔의 개수
TAG_LIMIT = 5


def create_tag(db: Session, tag_create: TagCreate):
    if db.query(Tag).filter(Tag.recipe_id == tag_create.recipe_id, Tag.tag_id == tag_create.tag_id).first():
        return

    db_tag = Tag(
        recipe_id=tag_create.recipe_id,
        tag_id=tag_create.tag_id,
    )
    db.add(db_tag)
    db.commit()


def get_existing_tag(db: Session, tag_name: str):
    return db.query(TagInfo).filter(TagInfo.name == tag_name).first()


def get_similar_tag_list(db: Session, limit: int = 5, keyword: str = ''):
    # keyword에 해당하는 태그들을 찾습니다.
    if keyword:
        tag_list = db.query(TagInfo).filter(TagInfo.name.like(f'%{keyword}%')).all()
    else:
        tag_list = db.query(TagInfo).all()

    # 태그들을 사용 이력이 가장 많은 순으로 정렬합니다.
    tag_list = sorted(tag_list, key=lambda tag: db.query(func.count(Tag.tag_id)).filter(Tag.tag_id == tag.id).scalar(),
                      reverse=True)

    # limit 값에 따라 반환할 태그의 개수를 제한합니다.
    tag_list = tag_list[:limit]

    return tag_list


def create_tag_info(db: Session, tag_info_create: TagInfoCreate):
    if get_existing_tag(db, tag_info_create.name):
        return

    db_tag_info = TagInfo(
        name=tag_info_create.name,
    )
    db.add(db_tag_info)
    db.commit()


def add_tag(db: Session, tag_list: AddTag):
    # 만약 recipe_id에 태그 개수가 TAG_LIMIT 이상이라면 추가할 수 없습니다.
    if db.query(func.count(Tag.tag_id)).filter(Tag.recipe_id == tag_list.recipe_id).scalar() >= TAG_LIMIT:
        return
    for tag_name in tag_list.tag_list:
        if not get_existing_tag(db, tag_name):
            create_tag_info(db, TagInfoCreate(name=tag_name))
        tag_id = get_existing_tag(db, tag_name).id
        create_tag(db, TagCreate(recipe_id=tag_list.recipe_id, tag_id=tag_id))


def delete_tag(db: Session, tag_id: int, recipe_id: int):
    db.query(Tag).filter(Tag.tag_id == tag_id, Tag.recipe_id == recipe_id).delete()
    db.commit()