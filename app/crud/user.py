import json
from typing import List, Optional, Dict, Any

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
    # 장르 목록을 JSON 문자열로 변환 - 유니코드 이스케이프 처리 안함
    # 이미 문자열인 경우 처리 
    if isinstance(user.genre, str):
        genre_json = user.genre
    else:
        try:
            genre_json = json.dumps(user.genre, ensure_ascii=False)
        except (TypeError, ValueError):
            # 어떤 이유로든 직렬화 실패 시 빈 리스트로 처리
            genre_json = "[]"
    
    db_user = User(
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
    
    # genre 필드가 있으면 JSON 문자열로 변환 - 유니코드 이스케이프 처리 안함
    if "genre" in update_data:
        if isinstance(update_data["genre"], str):
            pass  # 이미 문자열이면 처리하지 않음
        else:
            try:
                update_data["genre"] = json.dumps(update_data["genre"], ensure_ascii=False)
            except (TypeError, ValueError):
                # 어떤 이유로든 직렬화 실패 시 빈 리스트로 처리
                update_data["genre"] = "[]"
    
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