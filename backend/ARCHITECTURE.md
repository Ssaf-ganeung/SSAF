# Backend Architecture

## 1. 역할

백엔드는 다음 책임을 가진다.

- 지역 공공데이터 저장 및 조회
- 익명 커뮤니티 게시글 CRUD
- 작성 비밀번호 기반 수정·삭제 권한 확인
- OpenAI 기반 챗봇 API 제공
- SQLite 데이터베이스 연결 및 관리
- 프론트엔드 개발 서버에 대한 CORS 허용

## 2. 기술 스택

- FastAPI
- SQLAlchemy
- SQLite
- Pydantic Settings
- OpenAI Python SDK
- Uvicorn
- python-multipart

## 3. 디렉터리 구조

```text
backend/
├── ARCHITECTURE.md
├── CONSTRAINTS.md
├── requirements.txt
├── .env.example
├── data/
│   ├── SCHEMA.md
│   ├── SOURCE.md
│   └── 대전_충청권_*.json
├── docs/
│   ├── community-crud-backend.md
│   └── map-visualization-backend.md
└── app/
    ├── __init__.py
    ├── main.py
    ├── core/
    │   ├── __init__.py
    │   └── config.py
    ├── db/
    │   ├── __init__.py
    │   └── database.py
    ├── models/
    │   ├── __init__.py
    │   └── post.py
    ├── schemas/
    │   ├── __init__.py
    │   ├── chat.py
    │   ├── place.py
    │   └── post.py
    ├── crud/
    │   ├── __init__.py
    │   └── post.py
    ├── services/
    │   ├── __init__.py
    │   ├── chat_service.py
    │   └── place_service.py
    └── routers/
        ├── __init__.py
        ├── chat.py
        ├── place.py
        └── post.py
```

## 4. 레이어 구조

### `app/core`

환경 변수와 애플리케이션 설정을 관리한다.

`config.py`는 `pydantic-settings`의 `BaseSettings`를 사용한다.

관리 대상 값:

- `OPENAI_API_KEY`
- `DATABASE_URL`
- `CORS_ORIGINS`

### `app/db`

SQLAlchemy 연결 객체와 FastAPI DB 의존성을 관리한다.

`database.py` 책임:

- SQLAlchemy engine 생성
- `SessionLocal` 생성
- Declarative Base 생성
- 요청 단위 DB 세션을 제공하는 `get_db()` 정의

SQLite 사용을 위해 다음 옵션을 적용한다.

```python
connect_args={"check_same_thread": False}
```

### `app/models`

SQLAlchemy ORM 모델을 정의한다.

현재 구현 대상 모델:

- `Post`

공공데이터는 현재 SQLite ORM 모델로 적재하지 않고 `backend/data/`의 JSON을 읽기 전용으로 사용한다.

### `app/schemas`

API 요청·응답 Pydantic 스키마를 정의한다.

게시글 관련 스키마:

- `PostCreate`
- `PostUpdate`
- `PostDelete`
- `PostResponse`

지도 관련 스키마:

- `TourApiItem`: TourAPI `items` 원본 항목 검증
- `TourApiDataset`: JSON 파일 최상위 구조 검증
- `PlaceResponse`: 지도 표시용 정규화 응답
- `ContentTypeId`: 8개 TourAPI 콘텐츠 유형 ID
- `PlaceRegion`: 대전·세종·충북·충남·기타 권역

ORM 모델과 외부 API 스키마를 분리하여 비밀번호와 같은 내부 필드가 응답에 노출되지 않게 한다.

### `app/crud`

데이터베이스 조회와 변경 로직을 정의한다.

게시글 CRUD 함수:

- `get_posts`
- `get_post`
- `create_post`
- `update_post`
- `delete_post`

라우터는 HTTP 요청·응답 처리에 집중하고, DB 처리 로직은 CRUD 레이어에 위임한다.

### `app/services`

외부 SDK 연동과 JSON 기반 도메인 로직을 관리한다.

`place_service.py` 책임:

- 8개 TourAPI JSON 파일 경로 관리
- `TourApiDataset`을 사용한 원본 구조 검증
- 좌표 문자열의 `float` 변환
- 대전·충청권 서비스 좌표 경계 검사
- 주소 결합과 권역 판별
- `PlaceResponse` 변환
- 콘텐츠 유형 및 권역 필터

`place_data.py`는 챗봇용 JSON 캐시와 키워드 검색을 담당한다. 직전 추천 장소 ID를 후속 질문에 재사용하며, `가까운`, `근처`, `주변` 질문은 좌표 간 Haversine 직선거리로 정렬한다.

`chat_service.py`는 검색 결과를 답변 근거로 사용하고 OpenAI 답변을 일반 응답 또는 SSE 스트림으로 생성한다. 답변 근거와 프론트 지도 링크는 동일한 장소 목록을 사용한다.

공공데이터는 DB CRUD가 아니므로 `app/crud`가 아닌 `app/services`에서 처리한다.

### `app/routers`

FastAPI `APIRouter` 기반 엔드포인트를 정의한다.

현재 API prefix:

```text
/api/posts
/api/chat
/api/places
```

장소 라우터는 `content_type_id`와 `region` 쿼리 파라미터를 검증하고 장소 서비스에 조회를 위임한다.

챗봇 라우터는 일반 `POST /api/chat`, 스트리밍 `POST /api/chat/stream`, 검색 점검용 `GET /api/chat/search`를 제공한다.

### `app/main.py`

애플리케이션 진입점이다.

책임:

- FastAPI 인스턴스 생성
- CORS 미들웨어 등록
- `GET /` health check 제공
- `Base.metadata.create_all(bind=engine)` 호출
- 게시글 라우터 등록
- 챗봇 라우터 등록
- 장소 조회 라우터 등록

## 5. 공공데이터 지도 조회

### 데이터 유형

| ID   | 유형         |
| ---- | ------------ |
| `12` | 관광지       |
| `14` | 문화시설     |
| `15` | 축제공연행사 |
| `25` | 여행코스     |
| `28` | 레포츠       |
| `32` | 숙박         |
| `38` | 쇼핑         |
| `39` | 음식점       |

### 데이터 흐름

```text
backend/data JSON
→ TourApiDataset 검증
→ place_service 정규화 및 필터
→ GET /api/places
→ PlaceResponse[]
```

### 좌표 및 권역 처리

- `mapx`는 경도, `mapy`는 위도로 변환한다.
- 대전·충청권을 포함하는 사각형 좌표 경계 밖의 항목은 제외한다.
- 현재 원본 1,365건 중 잘못된 좌표 2건을 제외한 1,363건을 제공한다.
- `addr1`의 시작 문자열로 대전·세종·충북·충남을 판별한다.
- 주소로 판별할 수 없는 항목은 `기타`로 분류한다.
- 주소가 비어 있어도 유효한 서비스 권역 좌표를 가진 장소는 유지한다.

## 6. 커뮤니티 데이터 모델

### Post

| 필드         | 타입        | 설명                      |
| ------------ | ----------- | ------------------------- |
| `id`         | Integer, PK | 자동 증가 식별자          |
| `title`      | String      | 제목                      |
| `content`    | Text        | 본문                      |
| `password`   | String      | 수정·삭제 확인용 비밀번호 |
| `created_at` | DateTime    | 생성 시각                 |
| `updated_at` | DateTime    | 마지막 수정 시각          |

현재 게시판은 단일 권역 전용이므로 `category`와 `region` 컬럼을 두지 않는다.

## 7. REST API

| Method | Path              | 설명      | 요청 바디                      |
| ------ | ----------------- | --------- | ------------------------------ |
| GET    | `/api/posts`      | 목록 조회 | 없음                           |
| GET    | `/api/posts/{id}` | 상세 조회 | 없음                           |
| POST   | `/api/posts`      | 작성      | `{ title, content, password }` |
| PUT    | `/api/posts/{id}` | 수정      | `{ title, content, password }` |
| DELETE | `/api/posts/{id}` | 삭제      | `{ password }`                 |

지도 조회 API:

| Method | Path          | 설명           | Query                                      |
| ------ | ------------- | -------------- | ------------------------------------------ |
| GET    | `/api/places` | 장소 목록 조회 | `content_type_id`, `region` 모두 선택 사항 |

응답 규칙:

- 목록은 `created_at` 내림차순 정렬
- 없는 게시글은 `404 Not Found`
- 비밀번호 불일치는 `403 Forbidden`
- 모든 게시글 응답에서 `password` 제외

장소 조회 응답 규칙:

- 쿼리 파라미터가 없으면 8개 유형 전체를 반환
- 유형과 권역 조건은 함께 조합 가능
- 필터 결과가 없으면 `200 OK`와 빈 배열 반환
- 허용되지 않은 유형 또는 권역은 `422 Unprocessable Entity`
- 좌표, 이미지, 전화번호 등 지도 표시에 필요한 필드만 반환

## 8. 환경 변수

`.env.example` 기준:

```env
OPENAI_API_KEY=
DATABASE_URL=sqlite:///./app.db
CORS_ORIGINS=http://localhost:5173
```

`CORS_ORIGINS`는 쉼표로 구분된 문자열로 관리하고 앱 시작 시 리스트로 변환한다.

## 9. 초기 실행 검증

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

확인 주소:

- Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/`

## 10. 향후 확장

- 공공데이터 캐시 또는 DB 적재 전략
- 실제 행정구역 GeoJSON 기반 좌표 검증
- 게시글 페이지네이션
- 비밀번호 해시 전환
- 다중 권역 및 카테고리
- Alembic 기반 마이그레이션
- 테스트 코드
- Render 배포 설정
