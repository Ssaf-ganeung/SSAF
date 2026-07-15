from typing import Literal

from pydantic import BaseModel


class ChatMessage(BaseModel):
    """대화 한 줄. 프론트 Pinia store의 메시지와 동일한 모양."""
    role: Literal["user", "assistant"]
    content: str


class ChatRequest(BaseModel):
    """프론트가 보내는 요청. 대화 히스토리 전체를 배열로 받는다."""
    messages: list[ChatMessage]


class ChatResponse(BaseModel):
    """프론트가 읽는 응답. (ChatWidget.vue: response.data.reply)"""
    reply: str
