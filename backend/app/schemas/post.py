from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    """게시글 작성 요청 바디."""

    title: str
    content: str
    password: str


class PostUpdate(BaseModel):
    """게시글 수정 요청 바디. PUT은 title/content 전체 교체이므로 Create와 필드가 같다."""

    title: str
    content: str
    password: str


class PostDelete(BaseModel):
    """게시글 삭제 요청 바디. 삭제 권한 확인용 password만 받는다."""

    password: str


class PostResponse(BaseModel):
    """게시글 응답 바디. password는 절대 포함하지 않는다."""

    model_config = ConfigDict(from_attributes=True)  # SQLAlchemy Post 객체를 그대로 직렬화

    id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime | None
