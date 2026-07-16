from fastapi import APIRouter, Query

from app.schemas.place import (
    ContentTypeId,
    PlaceRegion,
    PlaceResponse,
)
from app.services.place_service import get_places


router = APIRouter(
    prefix="/api/places",
    tags=["places"],
)


@router.get("", response_model=list[PlaceResponse])
def list_places(
    content_type_id: ContentTypeId | None = Query(
        default=None,
        description="TourAPI 콘텐츠 유형 ID",
    ),
    region: PlaceRegion | None = Query(
        default=None,
        description="주소 기준 권역",
    ),
):
    """공공데이터 장소 목록을 콘텐츠 유형과 권역으로 필터링한다."""

    return get_places(
        content_type_id=content_type_id,
        region=region,
    )