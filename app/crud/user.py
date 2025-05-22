import json
from typing import List, Optional, Dict, Any

import nanoid
from sqlalchemy.orm import Session

from app.api.schemas.user import UserCreate, UserUpdate
from app.models.user import User


def get_user(db: Session, user_id: str) -> Optional[User]:
    """ID로 유저 조회"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_nickname(db: Session, nickname: str) -> Optional[User]:
    """닉네임으로 유저 조회"""
    return db.query(User).filter(User.nickname == nickname).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """모든 유저 조회"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """새 유저 생성"""
    genre_json = json.dumps(user.genre)  # 장르 목록을 JSON 문자열로 변환
    
    db_user = User(
        id=nanoid.generate(),
        nickname=user.nickname,
        gender=user.gender,
        genre=genre_json,
        favorite_movie=user.favorite_movie
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: str, user: UserUpdate) -> Optional[User]:
    """유저 정보 업데이트"""
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    
    update_data = user.model_dump(exclude_unset=True)
    
    # genre 필드가 있으면 JSON 문자열로 변환
    if "genre" in update_data:
        update_data["genre"] = json.dumps(update_data["genre"])
    
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: str) -> bool:
    """유저 삭제"""
    db_user = get_user(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True 