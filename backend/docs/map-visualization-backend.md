# 지도 시각화 Backend API

## 1. 목표

`backend/data/`에 저장된 TourAPI 4.0 공공데이터 JSON을 읽고,
지도 표시에 필요한 장소 데이터를 읽기 전용 API로 제공한다.

현재 보유한 다음 8개 콘텐츠 유형을 모두 구현 대상으로 한다.

| 콘텐츠 유형 ID | 콘텐츠 유형 |
| -------------- | ----------- |
| `12`           | 관광지      |
| `14`           | 문화시설    |
| `15`           | 축제공연행사 |
| `25`           | 여행코스    |
| `28`           | 레포츠      |
| `32`           | 숙박        |
| `38`           | 쇼핑        |
| `39`           | 음식점      |

공공데이터는 SQLite에 적재하지 않고 JSON 파일에서 직접 읽는다.
원본 JSON 파일은 수정하지 않는다.

## 2. 데이터 흐름

```text
backend/data JSON
→ TourApiDataset 원본 검증
→ place_service 정규화 및 필터링
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

| 이름              | 필수   | 허용 값                                          | 설명                     |
| ----------------- | ------ | ------------------------------------------------ | ------------------------ |
| `content_type_id` | 아니요 | `12`, `14`, `15`, `25`, `28`, `32`, `38`, `39` | TourAPI 콘텐츠 유형 ID   |
| `region`          | 아니요 | `대전`, `세종`, `충북`, `충남`, `기타`          | 주소에서 판별한 권역     |

쿼리 파라미터가 없으면 8개 JSON에 포함된 장소 전체를 반환한다.
두 파라미터를 함께 전달하면 두 조건을 모두 만족하는 장소만 반환한다.

### 요청 예시

전체 장소 조회:

```http
GET /api/places
```

관광지 조회:

```http
GET /api/places?content_type_id=12
```

음식점 조회:

```http
GET /api/places?content_type_id=39
```

대전 권역 조회:

```http
GET /api/places?region=대전
```

대전 권역의 음식점 조회:

```http
GET /api/places?content_type_id=39&region=대전
```

## 4. Response

정상 응답은 `200 OK`와 장소 배열을 반환한다.

```json
[
  {
    "id": "741957",
    "content_type_id": "12",
    "content_type": "관광지",
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

| 필드              | 타입   | 설명                                      |
| ----------------- | ------ | ----------------------------------------- |
| `id`              | string | TourAPI 장소 고유 ID                      |
| `content_type_id` | string | TourAPI 콘텐츠 유형 ID                    |
| `content_type`    | string | 화면에 표시할 콘텐츠 유형 한글 이름       |
| `title`           | string | 장소명                                    |
| `address`         | string | 기본 주소와 상세 주소를 결합한 값         |
| `region`          | string | 주소에서 판별한 권역                      |
| `latitude`        | number | 위도                                      |
| `longitude`       | number | 경도                                      |
| `image_url`       | string | 대표 이미지 URL, 없으면 빈 문자열         |
| `telephone`       | string | 전화번호, 없으면 빈 문자열                |

## 5. 원본 데이터 검증 및 변환 규칙

각 JSON 파일은 `TourApiDataset`으로 최상위 구조를 검증하고,
`items`의 각 항목은 `TourApiItem`으로 검증한다.

| 원본 필드        | 응답 필드         | 변환                                      |
| ---------------- | ----------------- | ----------------------------------------- |
| `contentid`      | `id`              | 문자열로 사용                             |
| `contenttypeid`  | `content_type_id` | 8개 허용 ID 중 하나인지 검증              |
| `contentType`    | `content_type`    | JSON 최상위의 한글 콘텐츠 유형 사용       |
| `title`          | `title`           | 그대로 사용                               |
| `addr1`, `addr2` | `address`         | 빈 값을 제외하고 공백으로 결합            |
| `addr1`          | `region`          | 주소 시작 문자열로 권역 판별              |
| `mapy`           | `latitude`        | 문자열을 실수로 변환                      |
| `mapx`           | `longitude`       | 문자열을 실수로 변환                      |
| `firstimage`     | `image_url`       | 없으면 빈 문자열                          |
| `tel`            | `telephone`       | 없으면 빈 문자열                          |

좌표 관계는 다음과 같다.

```text
mapx = 경도 = longitude
mapy = 위도 = latitude
Leaflet 좌표 순서 = [latitude, longitude]
```

## 6. 권역 판별 규칙

원본 데이터의 `areacode`가 비어 있는 항목이 있으므로 `addr1`의 시작 문자열로 권역을 판별한다.

| 주소 시작 문자열   | 권역   |
| ------------------ | ------ |
| `대전광역시`       | `대전` |
| `세종특별자치시`   | `세종` |
| `충청북도`         | `충북` |
| `충청남도`         | `충남` |
| 그 외 또는 빈 주소 | `기타` |

현재 데이터에는 세종 주소가 없어 `region=세종` 조회 결과가 빈 배열일 수 있다.

## 7. 예외 처리

- `mapx` 또는 `mapy`가 비어 있으면 해당 장소를 응답에서 제외한다.
- 좌표를 실수로 변환할 수 없으면 해당 장소를 응답에서 제외한다.
- `addr2`가 비어 있으면 `addr1`만 주소로 사용한다.
- 이미지가 없으면 `image_url`에 빈 문자열을 반환한다.
- 전화번호가 없으면 `telephone`에 빈 문자열을 반환한다.
- 주소로 권역을 판별할 수 없으면 `region`에 `기타`를 반환한다.
- 필터 결과가 없으면 `200 OK`와 빈 배열을 반환한다.
- 허용되지 않은 콘텐츠 유형 또는 권역은 FastAPI 요청 검증 오류 `422`로 처리한다.
- JSON 파일을 찾지 못하거나 원본 구조 검증에 실패하면 서버 오류로 처리한다.

## 8. 사용 데이터 파일

```text
backend/data/대전_충청권_관광지.json
backend/data/대전_충청권_문화시설.json
backend/data/대전_충청권_축제공연행사.json
backend/data/대전_충청권_여행코스.json
backend/data/대전_충청권_레포츠.json
backend/data/대전_충청권_숙박.json
backend/data/대전_충청권_쇼핑.json
backend/data/대전_충청권_음식점.json
```

8개 파일의 전체 원본 항목 수는 1,365개다.

## 9. 검증 결과

| 검증 항목                 | 기대 결과                 |
| ------------------------- | ------------------------- |
| 전체 조회                 | `200`, 1,365개            |
| 관광지 `12` 조회          | `200`, 335개              |
| 문화시설 `14` 조회        | `200`, 82개               |
| 축제공연행사 `15` 조회    | `200`, 26개               |
| 여행코스 `25` 조회        | `200`, 28개               |
| 레포츠 `28` 조회          | `200`, 68개               |
| 숙박 `32` 조회            | `200`, 52개               |
| 쇼핑 `38` 조회            | `200`, 258개              |
| 음식점 `39` 조회          | `200`, 516개              |
| 대전 권역 조회            | `200`, 851개              |
| 잘못된 콘텐츠 유형 `99`   | `422 Unprocessable Entity` |

Swagger UI는 다음 주소에서 확인한다.

```text
http://localhost:8000/docs
```
