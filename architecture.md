# 프로젝트 초기 세팅 설계 (모노레포: backend + frontend)

## Context
지자체 권역 공공데이터 기반 지역 정보 서비스(익명 커뮤니티 + AI 챗봇)를 개발하기 위한 신규 프로젝트. 요구사항(개발 요청 범위)은 Vue.js 3 SPA 프론트엔드, FastAPI+SQLAlchemy+SQLite 백엔드, OpenAI 기반 챗봇, Netlify/Render 배포를 명시하고 있다.

이번 초기 세팅 범위는 **git 연결 이전, 로컬 폴더/파일 기본 스캐폴딩**까지다. 실제 CRUD/챗봇 로직 구현, 배포 설정 파일, git init/remote 연결은 이후 별도 작업에서 진행한다. (CSS 프레임워크·배포 설정 파일 종류는 추후 결정)

확정된 스택:
- Frontend: Vue 3 + Vite, **JavaScript**(TS 아님), CSS 프레임워크 미정(추후 결정, 지금은 미설치)
- Backend: FastAPI + SQLAlchemy + SQLite, **venv + requirements.txt**
- 레포 구조: 모노레포, 루트에 `backend/`와 `frontend/`를 완전히 독립적으로 구성 (루트 통합 package.json 없음)

## 루트 구조
```
ssaf/
├── .gitignore
├── README.md
├── architecture.md
├── backend/
└── frontend/
```

## backend/ 구조
```
backend/
├── requirements.txt
├── .env.example
├── data/
│   └── .gitkeep          # 제공받을 공공데이터 JSON 저장 위치(추후 채움)
└── app/
    ├── __init__.py
    ├── main.py            # FastAPI 인스턴스, CORS 미들웨어, health check
    ├── core/
    │   ├── __init__.py
    │   └── config.py      # pydantic-settings 기반 Settings (.env 로드)
    ├── db/
    │   ├── __init__.py
    │   └── database.py    # SQLAlchemy engine/SessionLocal/Base/get_db
    ├── models/
    │   └── __init__.py    # 추후 posts, comments 등 정의 예정 (지금은 빈 패키지)
    ├── schemas/
    │   └── __init__.py
    ├── routers/
    │   └── __init__.py
    └── crud/
        └── __init__.py
```

- `requirements.txt`: fastapi, uvicorn[standard], sqlalchemy, pydantic-settings, openai, python-multipart
- `.env.example`:
  ```
  OPENAI_API_KEY=
  DATABASE_URL=sqlite:///./app.db
  CORS_ORIGINS=http://localhost:5173
  ```
- `config.py`: `Settings(BaseSettings)`로 위 3개 값 로드, `model_config = SettingsConfigDict(env_file=".env")`
- `database.py`: `create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})`, `SessionLocal`, `Base = declarative_base()`, `get_db()` 의존성 함수
- `main.py`: FastAPI 앱 생성, `CORSMiddleware`(allow_origins=settings.CORS_ORIGINS 파싱), `GET /` health check 엔드포인트. 라우터는 아직 구현 전이므로 include하지 않음(주석으로 위치만 표시).

## frontend/ 구조
`npm create vite@latest frontend -- --template vue` 로 JS 템플릿 생성 후, SPA 구조(커뮤니티 CRUD + 플로팅 챗봇)에 맞게 재구성:

```
frontend/
├── index.html
├── vite.config.js
├── package.json
├── .env.example              # VITE_API_BASE_URL=http://localhost:8000
└── src/
    ├── main.js                # createApp, router, pinia 등록
    ├── App.vue                # AppHeader/RouterView/ChatWidget 배치
    ├── router/
    │   └── index.js           # '/', '/community', '/community/:id', '/community/new', '/community/:id/edit'
    ├── stores/
    │   └── chat.js             # pinia store: 대화 히스토리(messages), 열림/닫힘 상태
    ├── views/
    │   ├── HomeView.vue
    │   └── community/
    │       ├── PostListView.vue    # 목록 조회 화면
    │       ├── PostDetailView.vue  # 상세 조회 + 수정/삭제 진입점
    │       └── PostFormView.vue    # 작성/수정 공용 폼(비밀번호 입력 포함)
    ├── components/
    │   ├── common/
    │   │   ├── AppHeader.vue
    │   │   └── AppFooter.vue
    │   ├── community/
    │   │   ├── PostCard.vue              # 목록의 게시글 1행/카드
    │   │   ├── PostForm.vue              # 제목/내용/비밀번호 입력 폼 컴포넌트
    │   │   └── PasswordConfirmModal.vue  # 수정·삭제 시 비밀번호 확인 모달
    │   └── chat/
    │       ├── ChatWidget.vue     # 우하단 플로팅 버튼 + 패널 토글 컨테이너
    │       ├── ChatWindow.vue     # 대화 히스토리 렌더링(스크롤 영역)
    │       ├── ChatMessage.vue    # 개별 메시지(user/assistant) 말풍선
    │       └── ChatInput.vue      # 입력창 + 전송 버튼
    ├── api/
    │   ├── client.js          # axios 인스턴스, baseURL = VITE_API_BASE_URL
    │   ├── posts.js           # 게시글 목록/상세/작성/수정/삭제 API 호출 함수
    │   └── chat.js            # POST /api/chat 호출 함수
    └── assets/                # 이미지, 전역 base css
```

- `vue-router`, `pinia`, `axios` 는 npm install로 추가
  - vue-router: 커뮤니티 목록/상세/작성/수정 등 다중 뷰 내비게이션에 필요
  - pinia: 플로팅 챗봇의 대화 히스토리를 페이지 이동과 무관하게 유지하기 위해 필요
  - axios: 백엔드 REST API(게시글 CRUD, /api/chat) 호출에 사용
- CSS 프레임워크는 설치하지 않고 Vite 기본 스타일만 유지 (추후 결정 예정이므로)
- 이 단계에서 각 `.vue`/`.js` 파일은 최소 골격(컴포넌트 선언 + 주석/TODO)만 작성하고, 실제 CRUD·API 연동 로직은 이후 기능 구현 단계에서 채운다

## 루트 파일
- `.gitignore`: backend/frontend 모두 커버 (node_modules, dist, venv, __pycache__, *.db, .env 등)
- `README.md`: 프로젝트 개요, 기술 스택, 폴더 구조, 로컬 실행 방법, 환경 변수 안내. "활용 데이터 목록" 및 "배포 URL" 섹션은 추후 채울 자리만 표시.
- `architecture.md`(본 문서): 왜 이렇게 구성했는지 + 전체 폴더 구조 설계를 담는 설계 문서.

## 다음 단계 (이번 세팅 범위 밖)
- 제공 JSON 데이터 수령 후 `backend/data/`에 배치, models/schemas/routers 구현
- 커뮤니티 CRUD API 및 화면 로직 구현
- `/api/chat` 챗봇 엔드포인트(OpenAI 연동) 구현
- CSS 프레임워크 결정 및 적용
- git init, GitHub remote 연결, push
- Netlify/Render 배포 설정 파일 작성 및 배포

## 검증
- Backend: `cd backend && python -m venv venv && venv 활성화 && pip install -r requirements.txt && uvicorn app.main:app --reload` 실행 후 `http://localhost:8000/docs`(Swagger UI)와 `GET /` 응답 확인
- Frontend: `cd frontend && npm install && npm run dev` 실행 후 `http://localhost:5173`에서 기본 화면 정상 렌더링 확인
