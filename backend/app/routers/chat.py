import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import generate_reply
from app.services.place_data import search_places
from app.services.place_service import detect_region, is_in_service_area
from app.services.chat_service import stream_reply

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest) -> ChatResponse:
    last_user_message = next(
        (
            message.content
            for message in reversed(payload.messages)
            if message.role == "user"
        ),
        "",
    )

    searched_places = search_places(last_user_message, limit=3)
    related_places = []

    for place in searched_places:
        try:
            latitude = float(place["lat"])
            longitude = float(place["lng"])
        except (TypeError, ValueError):
            continue

        if not is_in_service_area(
            latitude=latitude,
            longitude=longitude,
        ):
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

    reply = generate_reply(payload.messages)

    return ChatResponse(
        reply=reply,
        related_places=related_places,
    )


@router.get("/chat/search")
def search(q: str, limit: int = 8) -> list[dict]:
    """OpenAI 없이 키워드 검색 결과를 확인한다."""
    return search_places(q, limit)

@router.post("/chat/stream")
def stream_chat(payload: ChatRequest) -> StreamingResponse:
    last_user_message = next(
        (
            message.content
            for message in reversed(payload.messages)
            if message.role == "user"
        ),
        "",
    )

    searched_places = search_places(last_user_message, limit=3)
    related_places = []

    for place in searched_places:
        try:
            latitude = float(place["lat"])
            longitude = float(place["lng"])
        except (TypeError, ValueError):
            continue

        if not is_in_service_area(
            latitude=latitude,
            longitude=longitude,
        ):
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

    def generate_events():
        places_data = json.dumps(
            related_places,
            ensure_ascii=False,
        )

        yield f"event: places\ndata: {places_data}\n\n"

        for content in stream_reply(payload.messages):
            delta_data = json.dumps(
                {"content": content},
                ensure_ascii=False,
            )

            yield f"event: delta\ndata: {delta_data}\n\n"

        yield 'event: done\ndata: {}\n\n'

    return StreamingResponse(
        generate_events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        },
    )