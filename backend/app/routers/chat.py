import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatMessage, ChatRequest, ChatResponse
from app.services.chat_service import generate_reply, stream_reply
from app.services.place_data import search_chat_places, search_places
from app.services.place_service import detect_region, is_in_service_area

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


def normalize_related_places(places: list[dict]) -> list[dict]:
    related_places = []

    for place in places:
        try:
            latitude = float(place["lat"])
            longitude = float(place["lng"])
        except (KeyError, TypeError, ValueError):
            continue

        if not is_in_service_area(latitude=latitude, longitude=longitude):
            continue

        related_places.append(
            {
                "id": place["id"],
                "content_type_id": place["content_type_id"],
                "title": place["title"],
                "region": detect_region(place["addr"]),
                "latitude": latitude,
                "longitude": longitude,
            }
        )

    return related_places


def retrieve_places(payload: ChatRequest) -> list[dict]:
    return search_chat_places(
        query=get_last_user_message(payload.messages),
        previous_place_ids=get_previous_related_place_ids(payload.messages),
        limit=3,
    )


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    searched_places = retrieve_places(payload)

    return ChatResponse(
        reply=generate_reply(payload.messages, searched_places),
        related_places=normalize_related_places(searched_places),
    )


@router.get("/chat/search")
def search(q: str, limit: int = 8) -> list[dict]:
    """OpenAI 없이 키워드 검색 결과를 확인한다."""
    return search_places(q, limit)


@router.post("/chat/stream")
def stream_chat(payload: ChatRequest) -> StreamingResponse:
    searched_places = retrieve_places(payload)
    related_places = normalize_related_places(searched_places)

    def generate_events():
        places_data = json.dumps(related_places, ensure_ascii=False)
        yield f"event: places\ndata: {places_data}\n\n"

        for content in stream_reply(payload.messages, searched_places):
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
