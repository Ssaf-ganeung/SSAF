from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply
from app.services.place_data import search_places

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    # 4단계: 대화 히스토리 전체를 넘겨 맥락을 유지하며 답변(RAG + 멀티턴).
    reply = generate_reply(payload.messages)
    return ChatResponse(reply=reply)


@router.get("/chat/search")
def search(q: str, limit: int = 8) -> list[dict]:
    """[디버그] OpenAI 없이 키워드 검색 결과만 확인. 예: /api/chat/search?q=대전 관광지"""
    return search_places(q, limit)
