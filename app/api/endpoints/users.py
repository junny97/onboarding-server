import json
from typing import Any, List, Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from pydantic import parse_obj_as

from app.api.schemas.user import UserCreate, UserResponse, UserUpdate
from app.database.session import get_db
from app.crud import user as user_crud


router = APIRouter()


def process_user(user):
    """유저 데이터를 처리하는 함수"""
    if user is None:
        return None
    
    # genre 필드가 JSON 문자열이므로 파이썬 리스트로 변환
    if user.genre:
        try:
            # 이미 리스트인 경우 처리
            if isinstance(user.genre, list):
                pass
            # 문자열이 아닌 다른 타입인 경우 빈 리스트로 처리
            elif not isinstance(user.genre, str):
                user.genre = []
            # JSON 문자열 파싱 시도
            else:
                user.genre = json.loads(user.genre)
        except (json.JSONDecodeError, TypeError):
            user.genre = []
    else:
        user.genre = []
    
    return user


def process_users(users):
    """유저 리스트를 처리하는 함수"""
    result = []
    for user in users:
        result.append(process_user(user))
    return result


@router.post("/onboarding", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def onboarding(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate
) -> Any:
    """
    온보딩 정보 저장 (새 사용자만 생성)
    """
    # 닉네임 중복 확인
    user = user_crud.get_user_by_nickname(db, nickname=user_in.nickname)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 닉네임입니다."
        )
        
    # 새 사용자 생성
    created_user = user_crud.create_user(db=db, user=user_in)
    return process_user(created_user)


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    *,
    db: Session = Depends(get_db),
    user_id: int
) -> Any:
    """
    ID로 유저 조회
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저를 찾을 수 없습니다."
        )
    
    return process_user(user)


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate
) -> Any:
    """
    유저 정보 업데이트
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저를 찾을 수 없습니다."
        )
    
    # 닉네임이 변경되었고, 이미 해당 닉네임을 사용 중인 경우 체크
    if user_in.nickname and user_in.nickname != user.nickname:
        existing_user = user_crud.get_user_by_nickname(db, nickname=user_in.nickname)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 닉네임입니다."
            )
    
    user = user_crud.update_user(db=db, user_id=user_id, user=user_in)
    return process_user(user)


@router.delete("/{user_id}")
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int
) -> Any:
    """
    유저 삭제
    """
    user = user_crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저를 찾을 수 없습니다."
        )
    
    user_crud.delete_user(db=db, user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT) 