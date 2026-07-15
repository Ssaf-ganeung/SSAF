from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from app.db.database import Base


class Post(Base):
    """커뮤니티 게시글 테이블. 로그인 없이 password로만 수정/삭제 권한을 확인한다."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    # 평문 저장·평문 비교 (해시 없음 — 익명 게시판용 교육 목적의 의도된 설계)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
