from sqlalchemy import Column, Integer, String, Text

from app.database.base import Base


class User(Base):
    """유저 모델"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nickname = Column(String(50), unique=True, index=True, nullable=False)
    gender = Column(String(10), nullable=True)  # 'male' 또는 'female'
    genre = Column(Text, nullable=True)  # JSON 문자열로 저장 (SQLite에서는 ARRAY 타입 지원 안함)
    favorite_movie = Column(Text, nullable=True) 