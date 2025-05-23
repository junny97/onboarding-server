import os
import uvicorn

# 서버 구동 전에 데이터베이스 파일 존재 여부 확인
db_path = "onboarding.db"
if os.path.exists(db_path):
    try:
        # 배포 환경에서 자동으로 실행될 때만 기존 DB 삭제 (안전을 위해)
        if os.environ.get("RENDER") == "true":
            os.remove(db_path)
            print(f"Removed existing database file: {db_path}")
    except Exception as e:
        print(f"Warning: Could not remove database file: {e}")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 