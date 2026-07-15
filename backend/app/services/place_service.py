from pathlib import Path

from app.schemas.place import (
    ContentTypeId,
    PlaceRegion,
    PlaceResponse,
    TourApiDataset,
    TourApiItem,
)


DATA_DIR = Path(__file__).resolve().parents[2] / "data"

DATA_FILES = {
    "12": "대전_충청권_관광지.json",
    "14": "대전_충청권_문화시설.json",
    "15": "대전_충청권_축제공연행사.json",
    "25": "대전_충청권_여행코스.json",
    "28": "대전_충청권_레포츠.json",
    "32": "대전_충청권_숙박.json",
    "38": "대전_충청권_쇼핑.json",
    "39": "대전_충청권_음식점.json",
}

SERVICE_AREA_BOUNDS = {
    "min_latitude": 35.8,
    "max_latitude": 37.3,
    "min_longitude": 126.0,
    "max_longitude": 128.5,
}

def is_in_service_area(
    latitude: float,
    longitude: float,
) -> bool:
    """좌표가 대전·충청권 서비스 경계 안에 있는지 확인한다."""

    return (
        SERVICE_AREA_BOUNDS["min_latitude"]
        <= latitude
        <= SERVICE_AREA_BOUNDS["max_latitude"]
        and SERVICE_AREA_BOUNDS["min_longitude"]
        <= longitude
        <= SERVICE_AREA_BOUNDS["max_longitude"]
    )


def load_dataset(file_name: str) -> TourApiDataset:
    """공공데이터 JSON 파일 하나를 읽고 원본 스키마로 검증한다."""

    file_path = DATA_DIR / file_name
    json_text = file_path.read_text(encoding="utf-8")

    return TourApiDataset.model_validate_json(json_text)


def detect_region(address: str) -> PlaceRegion:
    """주소의 시작 문자열을 이용해 지도 필터용 권역을 반환한다."""

    if address.startswith("대전광역시"):
        return "대전"

    if address.startswith("세종특별자치시"):
        return "세종"

    if address.startswith("충청북도"):
        return "충북"

    if address.startswith("충청남도"):
        return "충남"

    return "기타"


def normalize_place(
    item: TourApiItem,
    content_type: str,
) -> PlaceResponse | None:
    """TourAPI 원본 항목을 지도 응답 형태로 변환한다."""

    try:
        longitude = float(item.mapx)
        latitude = float(item.mapy)
    except (TypeError, ValueError):
        return None

    if not is_in_service_area(
        latitude=latitude,
        longitude=longitude,
    ):
        return None

    address = " ".join(
        part.strip()
        for part in (item.addr1, item.addr2)
        if part.strip()
    )

    return PlaceResponse(
        id=item.contentid,
        content_type_id=item.contenttypeid,
        content_type=content_type,
        title=item.title,
        address=address,
        region=detect_region(item.addr1),
        latitude=latitude,
        longitude=longitude,
        image_url=item.firstimage,
        telephone=item.tel,
    )


def get_places(
    content_type_id: ContentTypeId | None = None,
    region: PlaceRegion | None = None,
) -> list[PlaceResponse]:
    """8개 JSON에서 장소를 읽고 선택된 조건으로 필터링한다."""

    places: list[PlaceResponse] = []

    for current_type_id, file_name in DATA_FILES.items():
        if content_type_id and current_type_id != content_type_id:
            continue

        dataset = load_dataset(file_name)

        for item in dataset.items:
            place = normalize_place(
                item=item,
                content_type=dataset.content_type,
            )

            if place is None:
                continue

            if region and place.region != region:
                continue

            places.append(place)

    return places
