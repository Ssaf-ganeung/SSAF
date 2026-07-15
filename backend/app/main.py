from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import Base, engine
from app.models.post import Post  # noqa: F401 (Base.metadata 등록을 위해 import)
from app.routers import post as post_router

app = FastAPI(title="ssaf API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 마이그레이션 도구 없이 앱 시작 시 테이블을 생성 (없는 테이블만 생성, 기존 테이블은 건드리지 않음)
Base.metadata.create_all(bind=engine)

app.include_router(post_router.router)


@app.get("/")
def health_check():
    return {"status": "ok"}
