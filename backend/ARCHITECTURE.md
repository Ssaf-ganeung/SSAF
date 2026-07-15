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
│   └── .gitkeep
├── docs/
│   └── community-crud-backend.md
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
    │   └── post.py
    ├── crud/
    │   ├── __init__.py
    │   └── post.py
    └── routers/
        ├── __init__.py
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

향후 공공데이터 구조가 확정되면 지역 정보용 모델을 추가한다.

### `app/schemas`

API 요청·응답 Pydantic 스키마를 정의한다.

게시글 관련 스키마:

- `PostCreate`
- `PostUpdate`
- `PostDelete`
- `PostResponse`

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

### `app/routers`

FastAPI `APIRouter` 기반 엔드포인트를 정의한다.

현재 커뮤니티 API prefix:

```text
/api/posts
```

### `app/main.py`

애플리케이션 진입점이다.

책임:

- FastAPI 인스턴스 생성
- CORS 미들웨어 등록
- `GET /` health check 제공
- `Base.metadata.create_all(bind=engine)` 호출
- 게시글 라우터 등록
- 향후 챗봇 라우터 등록 위치 제공

## 5. 커뮤니티 데이터 모델

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

## 6. REST API

| Method | Path              | 설명      | 요청 바디                      |
| ------ | ----------------- | --------- | ------------------------------ |
| GET    | `/api/posts`      | 목록 조회 | 없음                           |
| GET    | `/api/posts/{id}` | 상세 조회 | 없음                           |
| POST   | `/api/posts`      | 작성      | `{ title, content, password }` |
| PUT    | `/api/posts/{id}` | 수정      | `{ title, content, password }` |
| DELETE | `/api/posts/{id}` | 삭제      | `{ password }`                 |

응답 규칙:

- 목록은 `created_at` 내림차순 정렬
- 없는 게시글은 `404 Not Found`
- 비밀번호 불일치는 `403 Forbidden`
- 모든 게시글 응답에서 `password` 제외

## 7. 환경 변수

`.env.example` 기준:

```env
OPENAI_API_KEY=
DATABASE_URL=sqlite:///./app.db
CORS_ORIGINS=http://localhost:5173
```

`CORS_ORIGINS`는 쉼표로 구분된 문자열로 관리하고 앱 시작 시 리스트로 변환한다.

## 8. 초기 실행 검증

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

## 9. 향후 확장

- 공공데이터 JSON 모델 및 적재 로직
- 챗봇 `/api/chat` 라우터
- 게시글 페이지네이션
- 비밀번호 해시 전환
- 다중 권역 및 카테고리
- Alembic 기반 마이그레이션
- 테스트 코드
- Render 배포 설정
