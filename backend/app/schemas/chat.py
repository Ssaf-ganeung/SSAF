from typing import Literal

from pydantic import BaseModel, Field


class ChatRelatedPlace(BaseModel):
    id: str
    content_type_id: str
    title: str
    region: str
    latitude: float
    longitude: float


class ChatRelatedPost(BaseModel):
    """챗봇이 근거로 쓴 커뮤니티 게시글. 프론트는 이걸로 게시글 상세 링크를 만든다."""
    id: int
    title: str
    category: str


class ChatMessage(BaseModel):
    """대화 한 줄. 프론트 Pinia store의 메시지와 동일한 모양."""
    role: Literal["user", "assistant"]
    content: str
    related_places: list[ChatRelatedPlace] = Field(default_factory=list)


class ChatRequest(BaseModel):
    """프론트가 보내는 요청. 대화 히스토리 전체를 배열로 받는다."""
    messages: list[ChatMessage]

class ChatResponse(BaseModel):
    reply: str
    related_places: list[ChatRelatedPlace] = Field(default_factory=list)
    related_posts: list[ChatRelatedPost] = Field(default_factory=list)
