from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    # 2단계: OpenAI 호출로 실제 답변 생성. (3단계에서 지역 데이터 근거 추가 예정)
    reply = generate_reply(payload.message)
    return ChatResponse(reply=reply)
