# ssaf

지자체 권역 공공데이터 기반 지역 정보 서비스. 익명 커뮤니티(CRUD)와 AI 챗봇을 제공하는 SPA + REST API 프로젝트입니다.

전체 폴더 구조와 설계 배경은 [architecture.md](./architecture.md)를 참고하세요.

## 기술 스택
- Frontend: Vue.js 3 (Vite, JavaScript) + Vue Router + Pinia + Axios
- Backend: FastAPI + SQLAlchemy (ORM) + SQLite
- 챗봇: OpenAI API 연동 (`POST /api/chat`)
- 배포: Netlify(Frontend) / Render(Backend) — 추후 설정

## 폴더 구조
```
ssaf/
├── architecture.md   # 초기 설계 문서
├── backend/           # FastAPI 서버
└── frontend/          # Vue 3 SPA
```

## 로컬 실행 방법

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
pip install -r requirements.txt
cp .env.example .env         # 값 채워넣기
uvicorn app.main:app --reload
```
- API 문서: http://localhost:8000/docs

### Frontend
```bash
cd frontend
npm install
cp .env.example .env         # 값 채워넣기
npm run dev
```
- 개발 서버: http://localhost:5173

## 환경 변수
각 디렉터리의 `.env.example`을 복사해 `.env`로 만들고 값을 채워주세요. `.env`는 `.gitignore`에 등록되어 있어 저장소에 커밋되지 않습니다.

- `backend/.env`: `OPENAI_API_KEY`, `DATABASE_URL`, `CORS_ORIGINS`
- `frontend/.env`: `VITE_API_BASE_URL`

## 활용 데이터 목록
> 추후 제공받는 JSON 데이터 기준으로 출처·라이선스(공공누리 유형)·수집일을 정리 예정.

| 데이터명 | 출처 | 라이선스(공공누리 유형) | 수집일 | 비고 |
|---|---|---|---|---|
| TBD | | | | |

## 배포 URL
> 배포 완료 후 채울 예정.

- Frontend (Netlify): TBD
- Backend (Render): TBD
