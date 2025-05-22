import json
from typing import List, Optional
from pydantic import BaseModel, field_validator


class UserBase(BaseModel):
    """기본 유저 스키마"""
    nickname: str
    gender: Optional[str] = ""
    genre: Optional[List[str]] = []
    favorite_movie: Optional[str] = ""

    @field_validator('nickname')
    @classmethod
    def nickname_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('닉네임은 필수 입력값입니다')
        if len(v) < 2 or len(v) > 10:
            raise ValueError('닉네임은 2~10자 사이여야 합니다')
        return v.strip()
    
    @field_validator('gender')
    @classmethod
    def gender_must_be_valid(cls, v):
        if v and v not in ['male', 'female']:
            raise ValueError('성별은 male 또는 female이어야 합니다')
        return v


class UserCreate(UserBase):
    """유저 생성 스키마"""
    pass


class UserUpdate(BaseModel):
    """유저 업데이트 스키마"""
    nickname: Optional[str] = None
    gender: Optional[str] = None
    genre: Optional[List[str]] = None
    favorite_movie: Optional[str] = None

    @field_validator('nickname')
    @classmethod
    def nickname_must_be_valid(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('닉네임은 빈 값이 될 수 없습니다')
            if len(v) < 2 or len(v) > 10:
                raise ValueError('닉네임은 2~10자 사이여야 합니다')
            return v.strip()
        return v
    
    @field_validator('gender')
    @classmethod
    def gender_must_be_valid(cls, v):
        if v is not None and v not in ['male', 'female', '']:
            raise ValueError('성별은 male, female 또는 빈 값이어야 합니다')
        return v


class UserInDB(UserBase):
    """데이터베이스 유저 스키마"""
    id: int
    
    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    """유저 응답 스키마"""
    pass 