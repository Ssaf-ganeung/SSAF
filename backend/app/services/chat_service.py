"""챗봇 로직. 라우터는 요청만 받고, 실제 OpenAI 호출은 여기서 담당."""
from openai import OpenAI

from app.core.config import settings
from app.schemas.chat import ChatMessage
from app.services.place_data import format_context, resolve_intent, search_places
from app.services.post_search import format_post_context, has_post_intent, search_posts

# OpenAI에 보낼 대화 히스토리 최대 길이 (토큰/비용 폭주 방지)
MAX_HISTORY = 12

# 챗봇의 정체성/말투를 정하는 지시문.
SYSTEM_PROMPT = (
    "당신은 대전·충청권 지역 정보를 안내하는 '대·충 봇'입니다. "
    "동네 사정에 밝은 친구처럼, 밝고 친근한 존댓말로 이야기하세요.\n"
    "\n"
    "말투와 형식 규칙:\n"
    "- 채팅창이라 길면 읽지 않습니다. 짧게 답하세요.\n"
    "- **굵게**, # 제목, - 불릿은 쓰지 마세요. 화면에 기호가 그대로 보입니다.\n"
    "- 한두 곳만 말할 때는 목록 없이 '유성구 쪽이 무난한데, 리베라 호텔이 온천이랑 가까워요' "
    "처럼 말로 풀어서 이어 말하세요.\n"
    "- 세 개 이상을 나열하거나 사용자가 목록을 원하면, 한 줄에 하나씩 줄바꿈해서 "
    "'1. ', '2. ', '3. ' 처럼 숫자를 붙이세요. 한 항목은 한 줄로 짧게 쓰세요.\n"
    "- 이모지는 답변당 최대 1개까지만, 어울릴 때만 쓰세요.\n"
    "- '무엇을 도와드릴까요', '도움이 되었길 바랍니다', '~에 대해 안내해 드리겠습니다' 같은 "
    "형식적인 서론과 맺음말은 쓰지 마세요. 바로 본론부터 답하세요.\n"
    "- 사용자가 묻지 않은 정보를 덧붙이지 마세요.\n"
    "- 되물을 게 있으면 마지막에 짧은 질문 하나로 끝내세요.\n"
    "\n"
    "모르는 것은 지어내지 말고 솔직히 모른다고 말하세요."
)

# OpenAI 클라이언트는 한 번만 만들어 재사용 (요청마다 새로 만들 필요 없음)
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.OPENAI_API_KEY)
    return _client


def _build_system_prompt(message: str) -> str:
    """질문과 관련된 실제 장소·커뮤니티 게시글을 검색해 근거로 덧붙인다(RAG)."""
    place_context = format_context(search_places(message))

    # 게시글은 물어봤을 때만 붙인다. 장소 질문에 게시글이 섞이면 답이 흐려진다.
    post_context = ""
    if has_post_intent(message):
        post_context = format_post_context(search_posts(message))

    if not place_context and not post_context:
        return SYSTEM_PROMPT

    sections = [SYSTEM_PROMPT, ""]

    if place_context:
        sections.append(
            "다음은 사용자 질문과 관련된 대전·충청권의 실제 장소 목록(Context)입니다.\n"
            "- 반드시 이 Context 안의 데이터만 사용하세요. "
            "목록에 없는 장소나 숙소는 추천하지 마세요.\n"
            "- 추천은 최대 3개까지만 하세요.\n"
            "- 추천 이유는 한 줄씩만 쓰세요.\n"
            "- 사용자가 '그중', '주변 관광지'처럼 되물으면 새로운 숙소를 추천하지 말고, "
            "앞서 고른 숙소를 기준으로 Context 안의 관광지만 설명하세요.\n"
            "- 관련 정보가 부족하면 솔직히 없다고 답하세요.\n"
            f"{place_context}"
        )

    if post_context:
        sections.append(
            "다음은 사용자 질문과 관련된 커뮤니티 게시글 목록입니다. "
            "형식은 '[번호] 제목 (카테고리, 작성일) — 본문 일부' 입니다.\n"
            "- 게시글을 물어보면 이 목록만 근거로 답하고, 없는 글은 지어내지 마세요.\n"
            "- 제목과 함께 몇 번 글인지 번호를 알려주세요.\n"
            "- 최대 3개까지만 소개하세요.\n"
            "- 검색된 글이 없으면 아직 관련 게시글이 없다고 솔직히 답하세요.\n"
            f"{post_context}"
        )
    elif has_post_intent(message):
        # 검색은 했는데 결과가 0건인 경우. 이 말이 없으면 모델이 글을 지어낸다.
        sections.append(
            "사용자가 커뮤니티 게시글을 물었지만 검색 결과가 없습니다. "
            "관련 게시글이 아직 없다고 솔직히 답하세요. 게시글을 지어내지 마세요."
        )

    return "\n\n".join(sections)


def generate_reply(
    messages: list[ChatMessage],
    places: list[dict] | None = None,
) -> str:
    """대화 히스토리 전체를 받아 OpenAI 응답 텍스트를 돌려준다."""
    if not settings.OPENAI_API_KEY:
        return "(OpenAI API 키가 없습니다. backend/.env 의 OPENAI_API_KEY 를 채워주세요.)"
    if not messages:
        return "무엇이 궁금하신가요?"

    # 검색(RAG)은 가장 최근 사용자 메시지 기준으로 수행
    last_user = next((m.content for m in reversed(messages) if m.role == "user"), "")
    system_prompt = _build_system_prompt(last_user)

    # 최근 MAX_HISTORY개만 잘라서 맥락 유지 (오래된 대화는 버림)
    history = [{"role": m.role, "content": m.content} for m in messages[-MAX_HISTORY:]]

    try:
        completion = _get_client().chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "system", "content": system_prompt}, *history],
        )
        return completion.choices[0].message.content or ""
    except Exception as exc:  # 네트워크/키/쿼터 오류 등
        print(f"[chat_service] OpenAI 호출 실패: {exc}")
        return "죄송해요, 지금 답변을 생성하지 못했어요. 잠시 후 다시 시도해 주세요."

def stream_reply(
    messages: list[ChatMessage],
    places: list[dict] | None = None,
):
    if not settings.OPENAI_API_KEY:
        yield "(OpenAI API 키가 없습니다.)"
        return

    if not messages:
        yield "무엇이 궁금하신가요?"
        return

    # 검색(RAG)은 최근 사용자 메시지 기준. 유형·지역 힌트는 직전 질문들에서 물려받는다.
    recent_user_texts = [
        message.content for message in reversed(messages) if message.role == "user"
    ][:3]
    last_user = recent_user_texts[0] if recent_user_texts else ""

    system_prompt = _build_system_prompt(last_user)

    history = [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages[-MAX_HISTORY:]
    ]

    try:
        stream = _get_client().chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                *history,
            ],
            stream=True,
        )

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                yield content

    except Exception as exc:
        print(f"[chat_service] OpenAI 스트리밍 실패: {exc}")
        yield "죄송해요, 지금 답변을 생성하지 못했어요."
