from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """대화 한 줄. 프론트 Pinia store의 메시지와 동일한 모양."""
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """프론트가 보내는 요청. 대화 히스토리 전체를 배열로 받는다."""
    messages: list[ChatMessage]

    
class ChatRelatedPlace(BaseModel):
    id: str
    content_type_id: str
    title: str
    region: str
    latitude: float
    longitude: float


class ChatResponse(BaseModel):
    reply: str
    related_places: list[ChatRelatedPlace] = []
