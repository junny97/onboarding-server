from sqlalchemy import Column, String, Text, JSON

from app.database.base import Base


class User(Base):
    """유저 모델"""
    __tablename__ = "users"

    id = Column(String(21), primary_key=True, index=True)
    nickname = Column(String(50), unique=True, index=True, nullable=False)
    gender = Column(String(10), nullable=True)  # '남성' 또는 '여성'
    genre = Column(Text, nullable=True)  # JSON 문자열로 저장됨
    favorite_movie = Column(Text, nullable=True) 