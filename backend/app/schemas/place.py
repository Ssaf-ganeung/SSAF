from typing import Literal

from pydantic import BaseModel, Field


ContentTypeId = Literal[
    "12",
    "14",
    "15",
    "25",
    "28",
    "32",
    "38",
    "39",
]

ContentTypeName = Literal[
    "관광지",
    "문화시설",
    "축제공연행사",
    "여행코스",
    "레포츠",
    "숙박",
    "쇼핑",
    "음식점",
]

PlaceRegion = Literal[
    "대전",
    "세종",
    "충북",
    "충남",
    "기타",
]


class TourApiItem(BaseModel):
    """TourAPI JSON의 items 배열에 들어 있는 원본 장소."""

    contentid: str
    contenttypeid: ContentTypeId
    title: str
    addr1: str = ""
    addr2: str = ""
    mapx: str = ""
    mapy: str = ""
    firstimage: str = ""
    tel: str = ""


class TourApiDataset(BaseModel):
    """TourAPI JSON 파일의 최상위 구조."""

    region: str
    content_type: ContentTypeName = Field(alias="contentType")
    content_type_id: int = Field(alias="contentTypeId")
    total: int
    items: list[TourApiItem]


class PlaceResponse(BaseModel):
    """Leaflet 지도에 표시할 장소 응답."""

    id: str
    content_type_id: ContentTypeId
    content_type: ContentTypeName
    title: str
    address: str
    region: PlaceRegion
    latitude: float
    longitude: float
    image_url: str
    telephone: str