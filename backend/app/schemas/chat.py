from pydantic import BaseModel


class ChatRequest(BaseModel):
    """프론트가 보내는 요청 본문. (api/chat.js: { message })"""
    message: str


class ChatResponse(BaseModel):
    """프론트가 읽는 응답 본문. (ChatWidget.vue: response.data.reply)"""
    reply: str
