# 지도 시각화 Backend API

## 1. 목표

`backend/data/`에 저장된 TourAPI 4.0 공공데이터 JSON을 읽고,
지도 표시에 필요한 장소 데이터를 읽기 전용 API로 제공한다.

현재 1차 구현 대상은 다음 두 종류다.

- 관광지
- 음식점

공공데이터는 SQLite에 적재하지 않고 JSON 파일에서 직접 읽는다.

## 2. 데이터 흐름

```text
backend/data JSON
→ place_service
→ places router
→ GET /api/places
→ Frontend Axios
→ Leaflet Marker
```

## 3. Endpoint

```http
GET /api/places
```

### Query Parameters

| 이름     | 필수   | 허용 값                                | 설명           |
| -------- | ------ | -------------------------------------- | -------------- |
| `type`   | 아니요 | `tourist`, `food`                      | 장소 유형      |
| `region` | 아니요 | `대전`, `세종`, `충북`, `충남`, `기타` | 주소 기준 권역 |

파라미터가 없으면 관광지와 음식점 전체를 반환한다.

### 요청 예시

```http
GET /api/places
GET /api/places?type=tourist
GET /api/places?type=food
GET /api/places?region=대전
GET /api/places?type=food&region=대전
```

## 4. Response

정상 응답은 `200 OK`와 장소 배열을 반환한다.

```json
[
  {
    "id": "741957",
    "type": "tourist",
    "title": "대전솔로몬로파크",
    "address": "대전광역시 유성구 엑스포로 219-39 (원촌동)",
    "region": "대전",
    "latitude": 36.3773585309,
    "longitude": 127.4015597328,
    "image_url": "https://example.com/image.jpg",
    "telephone": ""
  }
]
```

### Response Fields

| 필드        | 타입   | 설명                              |
| ----------- | ------ | --------------------------------- |
| `id`        | string | 장소 고유 ID                      |
| `type`      | string | `tourist` 또는 `food`             |
| `title`     | string | 장소명                            |
| `address`   | string | 기본 주소와 상세 주소를 결합한 값 |
| `region`    | string | 주소에서 판별한 권역              |
| `latitude`  | number | 위도                              |
| `longitude` | number | 경도                              |
| `image_url` | string | 대표 이미지 URL, 없으면 빈 문자열 |
| `telephone` | string | 전화번호, 없으면 빈 문자열        |

## 5. 원본 데이터 변환 규칙

| 원본 필드        | 응답 필드   | 변환                           |
| ---------------- | ----------- | ------------------------------ |
| `contentid`      | `id`        | 문자열로 사용                  |
| `contenttypeid`  | `type`      | `12 → tourist`, `39 → food`    |
| `title`          | `title`     | 그대로 사용                    |
| `addr1`, `addr2` | `address`   | 빈 값을 제외하고 공백으로 결합 |
| `addr1`          | `region`    | 주소 시작 문자열로 판별        |
| `mapy`           | `latitude`  | 문자열을 실수로 변환           |
| `mapx`           | `longitude` | 문자열을 실수로 변환           |
| `firstimage`     | `image_url` | 없으면 빈 문자열               |
| `tel`            | `telephone` | 없으면 빈 문자열               |

좌표 관계:

```text
mapx = 경도 = longitude
mapy = 위도 = latitude
Leaflet 좌표 순서 = [latitude, longitude]
```

## 6. 권역 판별 규칙

| 주소 시작 문자열   | 권역   |
| ------------------ | ------ |
| `대전광역시`       | `대전` |
| `세종특별자치시`   | `세종` |
| `충청북도`         | `충북` |
| `충청남도`         | `충남` |
| 그 외 또는 빈 주소 | `기타` |

## 7. 예외 처리

- `mapx` 또는 `mapy`가 비어 있으면 해당 장소를 제외한다.
- 좌표를 실수로 변환할 수 없으면 해당 장소를 제외한다.
- `addr2`가 비어 있으면 `addr1`만 주소로 사용한다.
- 이미지가 없으면 `image_url`에 빈 문자열을 반환한다.
- 전화번호가 없으면 `telephone`에 빈 문자열을 반환한다.
- 주소로 권역을 판단할 수 없으면 `기타`로 분류한다.
- 원본 JSON은 읽기 전용으로 사용한다.
- 허용되지 않은 필터 값은 FastAPI 요청 검증 오류 `422`로 처리한다.

## 8. 사용 데이터 파일

```text
backend/data/대전_충청권_관광지.json
backend/data/대전_충청권_음식점.json
```

나머지 공공데이터 유형은 1차 구현에서 제외한다.
