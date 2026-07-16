import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
from app.services.chat_service import generate_reply, stream_reply
from app.services.place_data import search_chat_places, search_places
from app.services.place_service import detect_region, is_in_service_area
from app.services.post_search import POST_LINK_LIMIT, has_post_intent, search_posts

router = APIRouter(prefix="/api", tags=["chat"])


def get_last_user_message(messages: list[ChatMessage]) -> str:
    return next(
        (
            message.content
            for message in reversed(messages)
            if message.role == "user"
        ),
        "",
    )


def get_previous_related_place_ids(messages: list[ChatMessage]) -> list[str]:
    previous_assistant = next(
        (
            message
            for message in reversed(messages[:-1])
            if message.role == "assistant" and message.related_places
        ),
        None,
    )

    if previous_assistant is None:
        return []

    return [place.id for place in previous_assistant.related_places]


def is_linkable(place: dict) -> bool:
    """지도에 찍을 수 있는 장소인지. 좌표가 없거나 서비스 권역 밖이면 링크를 못 건다."""
    try:
        latitude = float(place["lat"])
        longitude = float(place["lng"])
    except (KeyError, TypeError, ValueError):
        return False
    return is_in_service_area(latitude=latitude, longitude=longitude)


def linkable_places(places: list[dict]) -> list[dict]:
    """링크를 걸 수 있는 장소만 남긴다.

    답변 근거와 링크를 같은 목록으로 맞추기 위한 것이다. 근거에는 있는데 링크에서
    걸러지면 "호텔 오노마 추천"해놓고 링크는 엉뚱한 곳으로 가게 된다.
    """
    return [place for place in places if is_linkable(place)]


def normalize_related_places(places: list[dict]) -> list[dict]:
    """이미 linkable_places로 걸러진 장소를 프론트가 쓰는 모양으로 바꾼다."""
    return [
        {
            "id": place["id"],
            "content_type_id": place["content_type_id"],
            "title": place["title"],
            "region": detect_region(place["addr"]),
            "latitude": float(place["lat"]),
            "longitude": float(place["lng"]),
        }
        for place in places
    ]


def retrieve_places(payload: ChatRequest) -> list[dict]:
    return search_chat_places(
        query=get_last_user_message(payload.messages),
        previous_place_ids=get_previous_related_place_ids(payload.messages),
        limit=3,
    )


def retrieve_posts(payload: ChatRequest) -> list[dict]:
    return search_posts(get_last_user_message(payload.messages), limit=POST_LINK_LIMIT)


def normalize_related_posts(posts: list[dict]) -> list[dict]:
    """게시글 상세로 링크할 수 있게 id/제목/카테고리만 추린다(본문은 링크에 불필요)."""
    return [
        {
            "id": post["id"],
            "title": post["title"],
            "category": post["category"],
        }
        for post in posts
    ]


def retrieve_context(payload: ChatRequest) -> tuple[list[dict], list[dict]]:
    """답변 근거로 쓸 (장소, 게시글)을 한 번만 검색한다.

    여기서 나온 목록이 곧 링크로도 나가므로, 답변과 링크가 항상 같은 곳을 가리킨다.
    게시글을 물으면 지도 링크는 주지 않는다.
    """
    if has_post_intent(get_last_user_message(payload.messages)):
        return [], retrieve_posts(payload)
    return linkable_places(retrieve_places(payload)), []


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    places, posts = retrieve_context(payload)

    return ChatResponse(
        reply=generate_reply(payload.messages, places, posts),
        related_places=normalize_related_places(places),
        related_posts=normalize_related_posts(posts),
    )


@router.get("/chat/search")
def search(q: str, limit: int = 8) -> list[dict]:
    """OpenAI 없이 키워드 검색 결과를 확인한다."""
    return search_places(q, limit)


@router.post("/chat/stream")
def stream_chat(payload: ChatRequest) -> StreamingResponse:
    places, posts = retrieve_context(payload)

    def generate_events():
        places_data = json.dumps(normalize_related_places(places), ensure_ascii=False)
        yield f"event: places\ndata: {places_data}\n\n"

        posts_data = json.dumps(normalize_related_posts(posts), ensure_ascii=False)
        yield f"event: posts\ndata: {posts_data}\n\n"

        # 답변도 위와 똑같은 places/posts만 근거로 쓴다 -> 링크와 절대 어긋나지 않는다.
        for content in stream_reply(payload.messages, places, posts):
            delta_data = json.dumps({"content": content}, ensure_ascii=False)
            yield f"event: delta\ndata: {delta_data}\n\n"

        yield "event: done\ndata: {}\n\n"

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )
