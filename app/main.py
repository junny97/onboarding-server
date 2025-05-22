from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.config import settings
from app.database.base import Base, engine

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# CORS 미들웨어 설정
origins = [
    "http://localhost:5173",  # 로컬 개발 서버
    "http://localhost:3000",  # 다른 가능한 로컬 포트
    "https://onboarding-client.vercel.app",  # 프론트엔드 배포 URL (있다면 변경)
    "*",  # 개발 환경에서는 모든 출처 허용
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
    expose_headers=["*"],  # 응답 헤더 노출
    max_age=86400,  # 프리플라이트 요청 캐시 시간 (24시간)
)

app.include_router(api_router, prefix=settings.API_PREFIX)


@app.get("/")
def root():
    return {"message": "온보딩 API에 오신 것을 환영합니다!"} 

@app.get("/ping")
def ping():
    """
    핑 엔드포인트 - 서버 상태 확인 및 슬립 모드 방지용
    """
    return {"status": "ok", "message": "Server is running"} 