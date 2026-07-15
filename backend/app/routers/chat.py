from fastapi import APIRouter

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply
from app.services.place_data import search_places

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    # 3단계: 관련 지역 데이터를 검색해 근거로 넣은 뒤 OpenAI가 답변(RAG).
    reply = generate_reply(payload.message)
    return ChatResponse(reply=reply)


@router.get("/chat/search")
def search(q: str, limit: int = 8) -> list[dict]:
    """[디버그] OpenAI 없이 키워드 검색 결과만 확인. 예: /api/chat/search?q=대전 관광지"""
    return search_places(q, limit)
