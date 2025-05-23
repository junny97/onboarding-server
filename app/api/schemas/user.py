import json
from typing import List, Optional
from pydantic import BaseModel, field_validator, Field


class UserBase(BaseModel):
    """기본 유저 스키마"""
    nickname: str = Field(..., description="사용자 닉네임", example="케시")
    gender: str = Field(..., description="성별 (남성 또는 여성)", example="남성")
    genre: List[str] = Field(..., description="선호 장르 목록", example=["로맨스", "코미디"])
    favorite_movie: str = Field(..., description="좋아하는 영화", example="어바웃타임")

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
        if not v or v not in ['남성', '여성']:
            raise ValueError('성별은 남성 또는 여성이어야 합니다')
        return v
    
    @field_validator('genre')
    @classmethod
    def genre_must_not_be_empty(cls, v):
        if not v or (len(v) == 1 and v[0] == ''):
            raise ValueError('최소 하나의 장르를 선택해야 합니다')
        return v
    
    @field_validator('favorite_movie')
    @classmethod
    def favorite_movie_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('좋아하는 영화는 필수 입력값입니다')
        if len(v.strip()) < 1:
            raise ValueError('좋아하는 영화명을 입력해주세요')
        return v.strip()


class UserCreate(UserBase):
    """유저 생성 스키마"""
    pass


class UserUpdate(BaseModel):
    """유저 업데이트 스키마"""
    nickname: Optional[str] = Field(None, description="사용자 닉네임", example="케시")
    gender: Optional[str] = Field(None, description="성별 (남성 또는 여성)", example="남성")
    genre: Optional[List[str]] = Field(None, description="선호 장르 목록", example=["로맨스", "코미디"])
    favorite_movie: Optional[str] = Field(None, description="좋아하는 영화", example="어바웃타임")

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
        if v is not None and v not in ['남성', '여성']:
            raise ValueError('성별은 남성 또는 여성이어야 합니다')
        return v
    
    @field_validator('genre')
    @classmethod
    def genre_must_be_valid(cls, v):
        if v is not None and (not v or (len(v) == 1 and v[0] == '')):
            raise ValueError('장르 목록이 제공된 경우 최소 하나의 장르가 있어야 합니다')
        return v
    
    @field_validator('favorite_movie')
    @classmethod
    def favorite_movie_must_be_valid(cls, v):
        if v is not None:
            if not v or not v.strip():
                raise ValueError('좋아하는 영화는 빈 값이 될 수 없습니다')
            if len(v.strip()) < 1:
                raise ValueError('좋아하는 영화명을 입력해주세요')
            return v.strip()
        return v


class UserInDB(UserBase):
    """데이터베이스 유저 스키마"""
    id: int = Field(..., description="사용자 고유 ID", example=1)
    
    class Config:
        from_attributes = True


class UserResponse(UserInDB):
    """유저 응답 스키마"""
    pass 