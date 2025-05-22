from typing import Generator

from app.database.base import SessionLocal


def get_db() -> Generator:
    """
    데이터베이스 세션을 생성하고 요청이 완료되면 닫는 의존성 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 