import enum

from sqlalchemy import Column, DateTime, Enum as SAEnum, Integer, String, Text
from sqlalchemy.sql import func

from app.db.database import Base


class PostCategory(str, enum.Enum):
    """게시글 카테고리. 고정된 8개 값만 허용한다."""

    TOURIST_SPOT = "관광지"
    LEISURE_SPORTS = "레포츠"
    CULTURAL_FACILITY = "문화시설"
    SHOPPING = "쇼핑"
    ACCOMMODATION = "숙박"
    TRAVEL_COURSE = "여행코스"
    RESTAURANT = "음식점"
    FESTIVAL_EVENT = "축제공연행사"


class Post(Base):
    """커뮤니티 게시글 테이블. 로그인 없이 password로만 수정/삭제 권한을 확인한다."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    # values_callable 없으면 DB에 멤버 .name(영문)이 저장되어 ?category=관광지 필터가 매치되지 않는다
    category = Column(
        SAEnum(
            PostCategory,
            name="post_category",
            values_callable=lambda enum_cls: [m.value for m in enum_cls],
        ),
        nullable=False,
    )
    # 평문 저장·평문 비교 (해시 없음 — 익명 게시판용 교육 목적의 의도된 설계)
    password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
