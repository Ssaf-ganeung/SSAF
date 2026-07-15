"""챗봇 로직. 라우터는 요청만 받고, 실제 OpenAI 호출은 여기서 담당."""
from openai import OpenAI

from app.core.config import settings
from app.services.place_data import search_places, format_context

# 챗봇의 정체성/말투를 정하는 지시문.
SYSTEM_PROMPT = (
    "당신은 대전·충청권 지역 정보를 안내하는 친절한 도우미 '대·충 봇'입니다. "
    "한국어로 간결하고 정확하게 답하세요. 모르면 모른다고 말하세요."
)

# OpenAI 클라이언트는 한 번만 만들어 재사용 (요청마다 새로 만들 필요 없음)
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def _build_system_prompt(message: str) -> str:
    """질문과 관련된 실제 장소를 검색해 시스템 프롬프트에 근거로 덧붙인다(RAG)."""
    places = search_places(message)
    context = format_context(places)
    if not context:
        return SYSTEM_PROMPT
    return (
        f"{SYSTEM_PROMPT}\n\n"
        "다음은 사용자 질문과 관련된 대전·충청권의 실제 장소 목록입니다. "
        "반드시 이 목록을 근거로 답하고, 목록에 없는 장소는 지어내지 마세요. "
        "관련 정보가 부족하면 솔직히 없다고 답하세요.\n"
        f"{context}"
    )


def generate_reply(message: str) -> str:
    """사용자 메시지 한 개를 받아 OpenAI 응답 텍스트를 돌려준다."""
    if not settings.OPENAI_API_KEY:
        return "(OpenAI API 키가 없습니다. backend/.env 의 OPENAI_API_KEY 를 채워주세요.)"

    try:
        completion = _get_client().chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": _build_system_prompt(message)},
                {"role": "user", "content": message},
            ],
        )
        return completion.choices[0].message.content or ""
    except Exception as exc:  # 네트워크/키/쿼터 오류 등
        print(f"[chat_service] OpenAI 호출 실패: {exc}")
        return "죄송해요, 지금 답변을 생성하지 못했어요. 잠시 후 다시 시도해 주세요."
