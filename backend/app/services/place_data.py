"""대전·충청권 관광 JSON 데이터 로딩 + 키워드 검색.

데이터가 1,365건뿐이라 벡터DB/임베딩 없이 단순 키워드 매칭으로 충분하다.
서버 시작 후 최초 1회만 파일을 읽어 메모리에 캐시한다.
"""
import json
from pathlib import Path

# 이 파일: backend/app/services/place_data.py → .parent 3번 = backend/ → /data
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

# 질문 속 키워드 → 콘텐츠 유형 힌트 (예: "맛집"이라 하면 음식점만 우선)
TYPE_HINTS = {
    "맛집": "음식점", "음식": "음식점", "식당": "음식점", "먹거리": "음식점",
    "축제": "축제공연행사", "행사": "축제공연행사", "공연": "축제공연행사",
    "숙박": "숙박", "호텔": "숙박", "펜션": "숙박", "모텔": "숙박", "잘": "숙박",
    "쇼핑": "쇼핑", "시장": "쇼핑", "마트": "쇼핑",
    "레포츠": "레포츠", "체험": "레포츠", "액티비티": "레포츠",
    "문화": "문화시설", "박물관": "문화시설", "미술관": "문화시설", "전시": "문화시설",
    "코스": "여행코스", "여행코스": "여행코스",
    "관광": "관광지", "명소": "관광지", "가볼": "관광지",
}

# 대전·충청권 지역명 (주소 매칭용). 긴 이름이 앞에 와야 "대전 서구"에서 "서구"가 먼저 잡힌다.
REGION_WORDS = [
    # 대전 자치구 — 사용자가 "서구", "동구"처럼 구 단위로 묻는 경우가 많다
    "동구", "중구", "서구", "유성구", "대덕구",
    # 광역 단위
    "대전", "세종", "충청", "충남", "충북",
    # 충남
    "천안", "공주", "보령", "아산", "서산", "논산", "계룡", "당진",
    "금산", "부여", "서천", "청양", "홍성", "예산", "태안",
    # 충북
    "청주", "충주", "제천", "보은", "옥천", "영동", "증평", "진천",
    "괴산", "음성", "단양",
]

# 광역 단위. 구/시/군이 함께 잡히면 이쪽은 버린다(_detect_regions 참고).
BROAD_REGIONS = {"대전", "세종", "충청", "충남", "충북"}

_places: list[dict] = []


def load_places() -> list[dict]:
    """모든 JSON을 읽어 필요한 필드만 추린 장소 리스트를 반환(최초 1회 캐시)."""
    global _places
    if _places:
        return _places

    places: list[dict] = []
    for path in sorted(DATA_DIR.glob("대전_충청권_*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        content_type = raw.get("contentType", "")
        for item in raw.get("items", []):
            places.append({
                "title": item.get("title", ""),
                "type": content_type,
                "addr": item.get("addr1", ""),
                "image": item.get("firstimage", ""),
                "lng": item.get("mapx", ""),
                "lat": item.get("mapy", ""),
            })
    _places = places
    print(f"[place_data] 장소 {len(places)}건 로드 완료")
    return _places


def _detect_type(query: str) -> str | None:
    for keyword, ctype in TYPE_HINTS.items():
        if keyword in query:
            return ctype
    return None


def _detect_regions(query: str) -> list[str]:
    """질문 속 지역명을 찾되, 구/시/군이 잡히면 광역 단위는 버린다.

    "대전 서구"에서 ["서구", "대전"]을 모두 쓰면 필터가 or 조건이라
    대전 전역이 통과해 서구 조건이 무의미해진다.
    """
    found = [r for r in REGION_WORDS if r in query]
    specific = [r for r in found if r not in BROAD_REGIONS]
    return specific or found


def resolve_intent(recent_user_texts: list[str]) -> tuple[str | None, list[str]]:
    """최근 사용자 메시지(최신순)에서 유형·지역 의도를 뽑는다.

    "맛집 추천해줘" → "서구에 있는 거" 처럼 후속 질문에 유형이 빠져도,
    직전 대화에서 유형을 물려받아 맥락을 유지한다. 최신 메시지가 항상 우선.
    """
    wanted_type: str | None = None
    regions: list[str] = []
    for text in recent_user_texts:  # 최신 → 과거 순
        if wanted_type is None:
            wanted_type = _detect_type(text)
        if not regions:
            regions = _detect_regions(text)
        if wanted_type and regions:
            break
    return wanted_type, regions


def search_places(
    query: str,
    limit: int = 8,
    wanted_type: str | None = None,
    regions: list[str] | None = None,
) -> list[dict]:
    """질문과 관련도가 높은 장소를 점수순으로 상위 limit개 반환.

    유형·지역이 주어지면 점수가 아니라 '필터'로 쓴다. "서구 맛집"을 물었는데
    점수만 매기면 다른 구의 장소가 섞여 들어오기 때문이다.
    """
    places = load_places()
    if wanted_type is None:
        wanted_type = _detect_type(query)
    if regions is None:
        regions = _detect_regions(query)
    # 조사(에서/의 등) 떼고 2글자 이상 토큰만 사용
    tokens = [t.strip(",.?!·")  for t in query.split() if len(t.strip(",.?!·")) >= 2]

    scored: list[tuple[int, dict]] = []
    for place in places:
        # 지역/유형을 지정했으면 해당하지 않는 장소는 아예 제외
        if regions and not any(r in place["addr"] for r in regions):
            continue
        if wanted_type and place["type"] != wanted_type:
            continue

        score = 0
        haystack = f"{place['title']} {place['addr']} {place['type']}"

        # 장소 이름이 질문에 직접 등장하면 강한 신호
        if len(place["title"]) >= 2 and place["title"] in query:
            score += 5
        # 일반 토큰 겹침
        for token in tokens:
            if token in haystack:
                score += 1

        # 필터를 통과한 것만 남았으므로, 토큰이 안 겹쳐도 후보로 인정
        if score > 0 or regions or wanted_type:
            scored.append((score, place))

    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [place for _, place in scored[:limit]]


def format_context(places: list[dict]) -> str:
    """검색된 장소들을 프롬프트에 넣을 텍스트로 변환."""
    if not places:
        return ""
    lines = []
    for p in places:
        line = f"- {p['title']} ({p['type']})"
        if p["addr"]:
            line += f" / 주소: {p['addr']}"
        lines.append(line)
    return "\n".join(lines)
